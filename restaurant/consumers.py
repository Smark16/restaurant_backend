import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Notification, User
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'user_{self.user_id}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user']

        await self.save_message(message, user_id)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'notification',
                'message': message,
                'user': user_id
            }
        )

    async def notification(self, event):
        message = event['message']
        user_id = event['user']

        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': message,
            'user': user_id
        }))

    @database_sync_to_async
    def save_message(self, message, user_id):
        user = User.objects.get(id=user_id)
        Notification.objects.create(user=user, message=message)
