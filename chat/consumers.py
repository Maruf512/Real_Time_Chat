import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
    
    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        user = self.scope['user']
        if user.is_authenticated:
            await self.save_message(user, message)
            await self.send_chat_message(user.username, message)


    @database_sync_to_async
    def save_message(self, user, message):
        Message.objects.create(author=user, content=message)


    async def send_chat_message(self, username, message):
        await self.send(text_data=json.dumps({
            'message': f"{username}: {message}"
        }))


