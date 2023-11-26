import json

from channels.db import database_sync_to_async
from django.db.models import Prefetch

from .models import Message, Chat
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room = await self.get_chat()
		self.user = self.scope['user']
		self.room_messages = await self.get_room_messages()

		# self.last_message = await self.get_last_message()
		self.room_group_name = f"chat_{self.room.name}"

		# Join room group
		await self.channel_layer.group_add(
			self.room_group_name, self.channel_name
		)
		await self.accept()

		await self.user_readed()

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
				'message_id': message.pk,
				"message": message.message,
				'author_id': self.user.id,
				'author_ava_url': message.author.avatar.url,
				'publish_date': message.pub_date.timestamp()
			}
		)

	# Receive message from room group
	async def chat_message(self, event):
		if self.check_user_message(event['author_id']):
			event['class'] = 'my-message'
		else:
			self.user_readed(event["message_id"])
			event['class'] = 'message-me'

		# Send message to WebSocket
		await self.send(text_data=json.dumps(event))

	@database_sync_to_async
	def get_chat(self):
		chat_name = self.scope["url_route"]["kwargs"]["room_name"]
		try:
			return Chat.objects.prefetch_related(
				Prefetch('messages', queryset=Message.objects.exclude(author=self.scope['user'].profile))
			).get(
				name=chat_name
			)
		except Chat.DoesNotExist:
			self.disconnect()

	@database_sync_to_async
	def get_last_message(self):
		return self.room.messages.all().order_by('-pub_date')[0]

	@database_sync_to_async
	def create_message(self, text_message: str):
		message = Message.objects.create(
			author=self.user.profile,
			message=text_message,
		)
		self.room.messages.add(message)
		return message

	def check_user_message(self, user_id):
		if user_id == self.user.id:
			return True
		return False

	@database_sync_to_async
	def new_last_message(self, message_id):
		message = Message.objects.get(id=message_id)

	@database_sync_to_async
	def get_room_messages(self):
		return self.room.messages.all()

	@database_sync_to_async
	def user_readed(self, message_id=None):
		if message_id:
			message = Message.objects.get(id=message_id)
			message.is_readed = True
			message.save()
		else:
			for i in self.room_messages:
				i.is_readed = True
				i.save()



