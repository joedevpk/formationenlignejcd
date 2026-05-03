import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from .models import Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        self.other_user_id = self.scope['url_route']['kwargs']['user_id']

        users = sorted([str(self.user.id), str(self.other_user_id)])
        self.room_group_name = f"chat_{users[0]}_{users[1]}"

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
        data = json.loads(text_data)

        message = data.get("message", "")
        file_url = data.get("file_url", None)
        file_type = data.get("file_type", "")

        if data.get("typing"):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "typing",
                    "sender": self.user.username
                }
            )
            return

        msg = await self.save_message(
            self.user.id,
            self.other_user_id,
            message,
            file_url,
            file_type
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": msg.content,
                "sender": self.user.username,
                "time": msg.timestamp.strftime("%H:%M"),
                "file_url": file_url,
                "file_type": file_type
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def typing(self, event):
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def save_message(self, sender_id, receiver_id, content, file_url=None, file_type=None):
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)

        # ⚠️ ici on garde seulement texte (UPLOAD doit être séparé HTTP)
        return Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=content
        )