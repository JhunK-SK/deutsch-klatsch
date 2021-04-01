from django.db import models
from django.conf import settings
from django.utils import timezone


class ChatRoom(models.Model):
    room_name = models.CharField(max_length=100, unique=True, blank=False)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        default=None,
    )
    
    def __str__(self):
        return 'Chat Room' + ' - ' + self.room_name


class ChatRoomMessage(models.Model):
    room_name = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message = models.TextField()
    writer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL
    )
    timestamp = models.DateTimeField(
        verbose_name='date created',
        default=timezone.now
    )
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        msg_writer = ''
        if self.writer == None:
            msg_writer = 'Ananymous User'
        else:
            msg_writer = self.writer.username

        return (
            msg_writer
            + ' -- at: '
            + self.room_name.room_name
            + ' -- msg: '
            + self.message
        )