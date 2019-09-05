from django.db import models
from django.contrib.auth.models import User


class Thread(models.Model):

    participants = models.ManyToManyField(User)
    created = models.DateTimeField('date published', auto_now_add=True)
    updated = models.DateTimeField('date updated', auto_now=True)

    def __str__(self):
        return 'Thread {} with users {}'.format(self.id, list(self.participants.values_list('username', flat=True)))


class Message(models.Model):

    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=300, )
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    created = models.DateTimeField('date published', auto_now_add=True)
    is_read = models.BooleanField(default=False)
