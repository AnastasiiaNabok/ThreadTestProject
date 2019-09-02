from django.contrib import admin

from .models import Thread
from .models import Message


class ThreadAdmin(admin.ModelAdmin):

    class Meta:
        verbose_name_plural = 'Threads'
        verbose_name = 'Thread'
        ordering = '-id'


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'thread', 'text', 'is_read', 'created')
    search_fields = ('sender', 'thread')

    class Meta:
        verbose_name_plural = 'Messages'
        verbose_name = 'Message'
        ordering = 'sender'


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message, MessageAdmin)
