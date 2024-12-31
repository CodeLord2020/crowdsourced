import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Conversation, Message, MessageRead
from .serializers import MessageSerializer
from django.utils import timezone

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return
    
        self.user_group = f"user_{self.user.id}"
        await self.channel_layer.group_add(
            self.user_group,
            self.channel_name
        )
        await self.accept()

        conversations = await self.get_user_conversations()
        for conversation_id in conversations:
            conversation_group = f"conversation_{conversation_id}"
            await self.channel_layer.group_add(
                conversation_group,
                self.channel_name
            )

    async def disconnect(self, close_code):
        if hasattr(self, 'user_group'):
            await self.channel_layer.group_discard(
                self.user_group,
                self.channel_name
            )
        
        # Clean up conversation subscriptions
        conversations = await self.get_user_conversations()
        for conversation_id in conversations:
            conversation_group = f"conversation_{conversation_id}"
            await self.channel_layer.group_discard(
                conversation_group,
                self.channel_name
            )
        
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        
        handlers = {
            'send_message': self.handle_send_message,
            'read_messages': self.handle_read_messages,
            'typing_status': self.handle_typing_status,
        }
        
        handler = handlers.get(action)
        if handler:
            await handler(data)
            

    async def handle_send_message(self, data):
        conversation_id = data.get('conversation')
        content = data.get('content')
        
        if not all([conversation_id, content]):
            return
        
        message = await self.create_message(conversation_id, content)
        if message:
            conversation_group = f"conversation_{conversation_id}"
            
            # Broadcast to conversation participants
            await self.channel_layer.group_send(
                conversation_group,
                {
                    "type": "chat.message",
                    "message": message
                }
            )

    async def handle_read_messages(self, data):
        conversation_id = data.get('conversation')
        if not conversation_id:
            return
            
        await self.mark_messages_read(conversation_id)
        
        # Broadcast read status to conversation participants
        conversation_group = f"conversation_{conversation_id}"
        await self.channel_layer.group_send(
            conversation_group,
            {
                "type": "messages.read",
                "user_id": str(self.user.id),
                "conversation_id": conversation_id,
                "timestamp": str(timezone.now())
            }
        )

    async def handle_typing_status(self, data):
        conversation_id = data.get('conversation')
        is_typing = data.get('is_typing', False)
        
        if not conversation_id:
            return
            
        conversation_group = f"conversation_{conversation_id}"
        await self.channel_layer.group_send(
            conversation_group,
            {
                "type": "typing.status",
                "user_id": str(self.user.id),
                "is_typing": is_typing
            }
        )

    async def chat_message(self, event):
        """Handler for chat messages"""
        await self.send(text_data=json.dumps({
            "type": "message",
            "data": event["message"]
        }))

    async def messages_read(self, event):
        """Handler for read receipts"""
        await self.send(text_data=json.dumps({
            "type": "read_receipt",
            "data": {
                "user_id": event["user_id"],
                "conversation_id": event["conversation_id"],
                "timestamp": event["timestamp"]
            }
        }))

    async def typing_status(self, event):
        """Handler for typing status updates"""
        await self.send(text_data=json.dumps({
            "type": "typing_status",
            "data": {
                "user_id": event["user_id"],
                "is_typing": event["is_typing"]
            }
        }))

    