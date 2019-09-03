from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from users.models import User


from .model_serializers import ThreadModelSerializer, MessageModelSerializer
from .view_serializers import ThreadCreateViewSerializer, MessageCreateViewSerializer


class CreateThreadView(APIView):
    view_request_serializer = ThreadCreateViewSerializer

    def post(self, request):
        serializer = self.view_request_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request_data = serializer.data
        member = User.objects.get(id=request_data.get('conversation_member'))
        create_thread_data = {"participants": [self.request.user, member]}
        model_serializer = ThreadModelSerializer(data=create_thread_data)
        model_serializer.is_valid(raise_exception=True)
        created_thread = model_serializer.save()
        return Response(ThreadModelSerializer(instance=created_thread).data, status=status.HTTP_201_CREATED)


class CreateMessageView(APIView):
    view_serializer = MessageCreateViewSerializer

    def post(self, request):
        serializer = self.view_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request_data = serializer.data
        model_serializer = MessageModelSerializer(data=request_data)
        model_serializer.is_valid(raise_exception=True)
        created_message = model_serializer.save()
        return Response(ThreadModelSerializer(instance=created_message).data, status=status.HTTP_201_CREATED)

