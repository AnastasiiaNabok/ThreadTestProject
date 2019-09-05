from rest_framework import serializers

from django.contrib.auth.models import User


class ThreadCreateViewSerializer(serializers.Serializer):
    conversation_member = serializers.IntegerField()

    def validate_conversation_member(self, conversation_member):
        if not User.objects.filter(id=conversation_member).exists():
            raise ValueError('Invalid member ID')
        else:
            return conversation_member


class MessageCreateViewSerializer(serializers.Serializer):
    sender = serializers.IntegerField()
    text = serializers.CharField(required=True)
    thread = serializers.IntegerField()
    is_read = serializers.BooleanField(default=False)


class MessageUpdateViewSerializer(serializers.Serializer):
    """ View Serializer for Message update"""

    message_ids = serializers.ListField(child=serializers.IntegerField())


class UnreadMessageViewSerializer(serializers.Serializer):
    """ View Serializer for Message update"""

    count = serializers.IntegerField()
