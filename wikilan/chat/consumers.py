import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import *

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_name = self.scope['url_route']['kwargs']['session_id']
        self.session_group = 'chat_%s' % self.session_name

        # await self.get_session()

        await self.channel_layer.group_add(self.session_group, self.channel_name)

        await self.accept()
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': 'Connected to session',
            'sender': 'users'
        }))

    async def disconnect(self):
        await self.channel_layer.group_discard(self.session_group, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        session = text_data_json['session']

        await self.save_message(sender, session, message)

        await self.channel_layer.group_send(
            self.session_group,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'session': session,
            }
        )
    
    async def chat_message(self, event):

        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': event['message'],
            'sender': event['sender']
        }))

    @sync_to_async
    def get_session(self):
        return Session.objects.get(id=self.session_name)

    @sync_to_async
    def save_message(self, sender, session, message):
        session = Session.objects.get(id=session)
        user = User.objects.get(username=sender)
        message = Message.objects.create(sender=user, session=session, content=message)
