
import json

from channels.db import database_sync_to_async

from .models import Message, Chat
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room = await self.get_chat()
        self.user = self.scope['user']
        # self.room_members = self.room.members.exclude(user=self.user)
        self.room_group_name = f"chat_{self.room.name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code=None):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = await self.create_message(text_data_json['message'])
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message",
                "message": message.message,
                'class': self.check_user_message(message),
                'author_ava_url': message.author.avatar.url
            }
        )

    # Receive message from room group
    async def chat_message(self, event):

        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_chat(self):
        chat_name = self.scope["url_route"]["kwargs"]["room_name"]
        try:
            return Chat.objects.get(
                name=chat_name
            )
        except Chat.DoesNotExist:
            self.disconnect()

    @database_sync_to_async
    def create_message(self, text_message: str):
        message = Message.objects.create(
            author=self.user.profile,
            message=text_message,
            group=self.room
        )
        return message

    def check_user_message(self, message):
        if message.author == self.user.profile:
            return 'my-message'
        return 'message-me'
