import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Notification, User
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Retrieve the user ID from the URL route
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        # Define room group based on user ID
        self.room_group_name = f'user_{self.user_id}'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        user_id = text_data_json.get('user')

        print(message, user_id)
        # Save the message to the database
        await self.save_message(message, user_id)

        # Broadcast the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'notification_message',
                'message': message,
                'user': user_id
            }
        )

    async def notification_message(self, event):
        message = event['message']
        user_id = event['user']

        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': message,
            'user': user_id
        }))

    @database_sync_to_async
    def save_message(self, message: str, user_id: int):
        try:
            user = User.objects.get(id=user_id)
            Notification.objects.create(user=user, message=message)
        except User.DoesNotExist:
            # Handle the case where the user does not exist
            pass
