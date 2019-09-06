from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.base import ObjectDoesNotExist
from .models import Thread, Message
from rest_framework.pagination import LimitOffsetPagination


from .model_serializers import ThreadModelSerializer, MessageModelSerializer
from .view_serializers import ThreadCreateViewSerializer, MessageUpdateViewSerializer, ThreadValidatorViewSerializer


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

    def delete(self, request):
        serializer = ThreadValidatorViewSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        thread = Thread.objects.get(pk=serializer.data.get('thread'))
        if self.request.user not in thread.participants.all():
            raise ValueError("No permissions fot this thread")
        thread.delete()
        return Response()


class GetAllThreadsForUserApiView(generics.GenericAPIView):
    """ Get all Threads and last message if available for authenticated User API """

    serializer_class = MessageModelSerializer
    pagination_class = LimitOffsetPagination

    def get(self, request):
        threads = Thread.objects.filter(participants=request.user)
        resp_data = dict()
        for thread in threads:
            try:
                last_message = thread.message_set.latest('created').text
                resp_data[thread.id] = last_message
            except ObjectDoesNotExist:
                resp_data[thread.id] = 'No Messages in this Thread'
        return Response(data=resp_data)


class UnreadMessagesAPIView(generics.GenericAPIView):
    """  This view return count of unread messages for authenticated user by thread """
    serializer_class = MessageModelSerializer

    def get(self, request):
        threads = Thread.objects.filter(participants=request.user)
        resp_data = dict()
        for thread in threads:
            count = thread.message_set.exclude(sender=request.user, is_read=True).count()
            resp_data[thread.id] = count
        return Response(data=resp_data)


class CreateMessageView(generics.CreateAPIView):
    """  Create Message API """
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


class ThreadMessagesAPIView(APIView, LimitOffsetPagination):
    """ Thread API"""
    serializer_class = ThreadModelSerializer

    def get(self, request):
        """
         This view should return a list of all messages from thread
        """
        serializer = ThreadValidatorViewSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        thread = Thread.objects.get(pk=serializer.data.get('thread'))

        if self.request.user not in thread.participants.all():
            raise ValueError("No permissions fot this thread")
        messages = thread.message_set.all()
        results = self.paginate_queryset(messages, request, view=self)
        serializer = MessageModelSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

# class ThreadMessagesAPIView(generics.ListAPIView):
#     """ Thread  API"""
#     queryset = Thread.objects.all()
#     serializer_class = ThreadModelSerializer
#     pagination_class = LimitOffsetPagination
#
#     def get(self, request):
#         """
#             This view should return a list of all messages from thread
#         """
#         serializer = ThreadValidatorViewSerializer(data=self.request.GET)
#         serializer.is_valid(raise_exception=True)
#         thread = Thread.objects.get(pk=serializer.data.get('thread'))
#
#         if self.request.user not in thread.participants.all():
#             raise ValueError("No permissions fot this thread")
#         messages = thread.message_set.all()
#         serializer = MessageModelSerializer(messages, many=True)
#         return Response(serializer.data)
