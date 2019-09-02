from rest_framework import serializers


from .models import Thread, Message, User


class MessageSerializer(serializers.ModelSerializer):
    pass


class ThreadSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True, source='message_set')

    class Meta:
        model = Thread
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    treads = serializers.SerializerMethodField()

    """ Method return tread Id and message"""

    def get_treads(self, user):
        return user.thread_set.all().values('id', 'message')

    class Meta:
        model = User
        fields = ('id', 'username', 'treads')
