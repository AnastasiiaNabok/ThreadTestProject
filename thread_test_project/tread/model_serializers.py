from rest_framework import serializers


from .models import Thread, Message


class MessageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


# class UserSerializer(serializers.ModelSerializer):
#     treads = serializers.SerializerMethodField()
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'treads')


# class ThreadSerializer(serializers.ModelSerializer):
#     messages = MessageSerializer(many=True, read_only=True, source='message_set')
#     participants = UserSerializer(many=True, read_only=True, source='user_set')
#
#     class Meta:
#         model = Thread
#         fields = '__all__'

class ThreadModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'

    def create(self, validated_data):
        filter_set = Thread.objects.filter(participants=validated_data.get('participants'))
        if filter_set.exists():
            return filter_set.first()
        else:
            return Thread.objects.create(**validated_data)


