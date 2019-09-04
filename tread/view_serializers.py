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

    sender = serializers.IntegerField(required=False)
    text = serializers.CharField(required=False)
    thread = serializers.IntegerField(required=False)
    is_read = serializers.BooleanField(required=True)
