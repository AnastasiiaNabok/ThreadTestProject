from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Thread, Message


from .model_serializers import ThreadModelSerializer, MessageModelSerializer
from .view_serializers import ThreadCreateViewSerializer, UnreadMessageViewSerializer, MessageUpdateViewSerializer


class CreateThreadView(APIView):
    """ Thread Create or Return existing API """
    view_request_serializer = ThreadCreateViewSerializer

    def post(self, request):
        serializer = self.view_request_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request_data = serializer.data
        create_thread_data = {"participants": [self.request.user.id,
                                               request_data.get('conversation_member')]}
        model_serializer = ThreadModelSerializer(data=create_thread_data)
        model_serializer.is_valid(raise_exception=True)
        created_thread = model_serializer.save()
        return Response(ThreadModelSerializer(instance=created_thread).data, status=status.HTTP_201_CREATED)


class DeleteThreadAPI(APIView):
    """ Thread Delete API """
    view_request_serializer = ThreadModelSerializer

    def delete(self, request, pk):
        thread = Thread.objects.get(pk=pk)
        print(self.request.user)
        if self.request.user not in thread.participants.all():
            raise ValueError("No permissions fot this thread")
        thread.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetAllThreadsForUserApiView(APIView):
    """ Get all Threads for User API """

    queryset = Thread.objects.all()
    serializer_class = ThreadModelSerializer

    def get_queryset(self):
        """
         This view should return a list of all threads
        for the currently authenticated user.
        """
        user = self.request.user.thread_set.all()
        return user


class UnreadMessagesAPIView(generics.GenericAPIView):
    """  This view should return count of unread messages for user """
    serializer_class = MessageModelSerializer

    def get(self, request):
        threads = Thread.objects.filter(participants=request.user)
        count = 0
        for thread in threads:
            count += Message.objects.filter(thread=thread.id).filter(sender=(not request.user)).filter(is_read=False).count()
        return Response(data={'count': count})


class CreateMessageView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageModelSerializer


class MessageUpdateView(APIView):
    """ Message Update API with partial update"""
    view_request_serializer = MessageUpdateViewSerializer

    def put(self, request):
        serializer = self.view_request_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request_data = serializer.data
        resp_data = list()
        for message_id in request_data.get('message_ids'):
            message = Message.objects.get(id=message_id)
            serializer = MessageModelSerializer(instance=message, data={'is_read': True}, partial=True)
            serializer.is_valid(raise_exception=True)
            resp_data.append(serializer.save())
        return Response(MessageModelSerializer(resp_data, many=True).data)
