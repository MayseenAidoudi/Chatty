import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Count
from .models import  Message,User,Chat
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self): 
        self.username_b = self.scope['url_route']['kwargs']['username_link']
        self.username_a = self.scope['user'].username
        
        # Check if user_a and user_b are friends (implement your logic here)
        # If not friends, reject the connection
        
        sorted_usernames = sorted([self.username_a, self.username_b])
        self.room_group_name = f"chat_{sorted_usernames[0]}_{sorted_usernames[1]}"

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
        sender = self.username_a  # Set the sender as the current user's username
        Sender = self.scope['user']
        await self.save_message(Sender, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )
    @database_sync_to_async
    def save_message(self, Sender, message):
        user_b = User.objects.get(username = self.username_b)
        chatrec  = Chat.objects.annotate(participant_count=Count('participants')).filter(participants=Sender).filter(participants=user_b).filter(participant_count=2)
        if chatrec.exists():
            message = Message.objects.create(
                user=Sender,
                chat=chatrec.get(),  # Update this based on your logic
                text=message
            )
        else:
            chat_to = Chat.objects.create()
            chat_to.participants.add(user_b)
            chat_to.participants.add(Sender)
            chat_to.save()
            message = Message.objects.create(
                user=Sender,
                chat=chat_to,  # Update this based on your logic
                text=message
            )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

class DefaultConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.close()

