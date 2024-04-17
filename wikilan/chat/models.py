from django.db import models
from django.contrib.auth.models import User
import uuid


# session : chat 
class Session(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, auto_created=True, default=uuid.uuid4, max_length=16)
    name = models.CharField(blank=True, max_length=64)
    description = models.TextField(blank=True, max_length=256)
    is_open = models.BooleanField(default=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='admin_sessions')
    timestamp = models.DateTimeField(auto_now_add=True)
    allowed = models.ManyToManyField(User, related_name='allowed_sessions', blank=True, default=all)  # users allowed to join the session
    can_chat = models.ManyToManyField(User, related_name='chat_sessions', blank=True, default=all)  # users allowed to chat 
    reply_to = models.ForeignKey(User, related_name='replies', on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return f"{self.name}|{self.id}"

# message : chat
class Message(models.Model):
    session = models.ForeignKey(Session, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.sender}"


class SessionUploads(models.Model):
    session = models.ForeignKey(Session, related_name='uploads', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='uploads', on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}|{self.session}"

class MessageThread(models.Model):
    user = models.ForeignKey(User, related_name='threads', on_delete=models.CASCADE, null=True, blank=True)
    id = models.AutoField(primary_key=True, unique=True, auto_created=True)
    content = models.TextField(max_length=50, default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    # thread_key = models.IntegerField(default=id)

    class Meta:
        ordering = ['timestamp']

class ThreadReply(models.Model):
    key = models.IntegerField(null=False, default=0)
    # thread = models.ForeignKey(MessageThread, related_name='t_replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='t_replies', on_delete=models.CASCADE)
    content = models.TextField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}|{self.thread}"

# TODO: 
    # 1. add voice channels and in session voice communication feature
    # 2. add functionality to send invites, see session activity logs for session admin, entry loga, banning, muting...
    # 3. add functionality to send voice messages
    # 4. add functionality to clear chat session after session ends, and make option
    # 5. deal with processes that could be automated using Redis, Celery, RabbitMQ, and other tools
    # 6. add functionality make a request before joining a session
    ... 