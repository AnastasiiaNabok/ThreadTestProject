from rest_framework import serializers

from django.contrib.auth.models import User


class ThreadCreateViewSerializer(serializers.Serializer):
    """ View Serializer for Thread create. Validate if the member exist """
    conversation_member = serializers.IntegerField()

    def validate_conversation_member(self, conversation_member):
        if not User.objects.filter(id=conversation_member).exists():
            raise ValueError('Invalid member ID')
        else:
            return conversation_member


class MessageCreateViewSerializer(serializers.Serializer):
    """ View Serializer for Message create"""
    sender = serializers.IntegerField()
    text = serializers.CharField(required=True)
    thread = serializers.IntegerField()
    is_read = serializers.BooleanField(default=False)


class MessageUpdateViewSerializer(serializers.Serializer):
    """ View Serializer for Message update"""

    message_ids = serializers.ListField(child=serializers.IntegerField())


class ThreadValidatorViewSerializer(serializers.Serializer):

    thread = serializers.IntegerField()
