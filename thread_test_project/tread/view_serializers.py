from rest_framework import serializers


from django.contrib.auth.models import User
from .models import Thread


class ThreadCreateViewSerializer(serializers.Serializer):
    conversation_member = serializers.IntegerField()

    def validate_member(self, conversation_member):
        if not User.objects.filter(id=conversation_member).exists():
            raise ValueError('Invalid member ID')
        else:
            return conversation_member


class MessageCreateViewSerializer(serializers.Serializer):
    sender = serializers.IntegerField()
    text = serializers.CharField(required=True)
    thread = serializers.IntegerField()
    is_read = serializers.BooleanField(default=False)

    # def validate_sender_in_thread(self, sender):
    #     if not Thread.objects.filter(participant=sender).exists():
    #         raise ValueError('This sender is not thread member')
    #     else:
    #         return sender
