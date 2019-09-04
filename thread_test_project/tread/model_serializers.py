from rest_framework import serializers


from .models import Thread, Message


class MessageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

    thread_for_sender = serializers.SerializerMethodField()

    def get_thread_for_sender(self, request):
        try:
            participants = Thread.objects.get(id=request.thread.id).participants.all()
            if request.sender not in participants:
                raise Exception
        except Exception:
            raise ValueError('No such thread.')


class ThreadModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        participants_ids_list = [el.id for el in participants]
        queryset = Thread.objects.filter(participants=participants_ids_list[0]
                                         ).filter(participants=participants_ids_list[1])
        if queryset.exists():
            return queryset.first()
        else:

            thread = Thread.objects.create(**validated_data)
            thread.participants.add(*participants)
            return thread
