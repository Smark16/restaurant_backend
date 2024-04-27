import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Notification, User
from django.contrib.auth.models import AbstractUser

class ChatConsumer(WebsocketConsumer):
    def connect(self):
       self.room_group_name = 'test'
       async_to_sync(self.channel_layer.group_add)(
           self.room_group_name,
           self.channel_name
       )
       
       self.accept()

    def disconnect(self):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
       
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user']

        print(user_id)

        async_to_sync(self.save_message(message, user_id))
       
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'notification',
                'message':message
            }
        )

    def notification(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type':'notification',
            'message':message
        }))

    
    def save_message(self, message, user_id):
        user = User.objects.get(id=user_id)
        Notification.objects.create(user=user, message=message)