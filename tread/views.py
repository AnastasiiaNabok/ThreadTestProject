from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Thread, Message


from .model_serializers import ThreadModelSerializer, MessageModelSerializer
from .view_serializers import ThreadCreateViewSerializer, MessageCreateViewSerializer, MessageUpdateViewSerializer


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


class CreateMessageView(APIView):
    """ Message Create API """
    view_serializer = MessageCreateViewSerializer

    def post(self, request):
        serializer = self.view_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request_data = serializer.data
        model_serializer = MessageModelSerializer(data=request_data)
        model_serializer.is_valid(raise_exception=True)
        created_message = model_serializer.save()
        return Response(MessageModelSerializer(instance=created_message).data, status=status.HTTP_201_CREATED)


class MessageUpdateView(APIView):
        """ Message Update API with partial update"""
        view_request_serializer = MessageUpdateViewSerializer

        def put(self, request, pk):
            serializer = self.view_request_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            message = get_object_or_404(Message.objects.all(), pk=pk)
            request_data = serializer.data
            serializer = MessageModelSerializer(instance=message, data=request_data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_message = serializer.save()
            return Response(MessageModelSerializer(instance=updated_message).data)
