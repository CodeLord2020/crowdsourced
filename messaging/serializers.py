
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message, Conversation

User = get_user_model()



class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user information for messaging context"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'profile_picture']
        read_only_fields = fields



class MessageSerializer(serializers.ModelSerializer):
    """Serializer for message objects"""
    sender = UserBasicSerializer(read_only=True)
    read_by = UserBasicSerializer(many=True, read_only=True)
    is_read = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = [
            'id', 'conversation', 'sender', 'content',
            'created_at', 'updated_at', 'is_edited',
            'is_deleted', 'deleted_at', 'read_by', 'is_read'
        ]
        read_only_fields = [
            'id', 'sender', 'created_at', 'updated_at',
            'is_edited', 'is_deleted', 'deleted_at', 'read_by'
        ]

    def get_is_read(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return obj.read_by.filter(id=request.user.id).exists()
        return False
    


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for conversation objects"""
    participants = UserBasicSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'participants', 'created_at', 'updated_at',
            'is_active', 'last_message', 'unread_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        last_message = obj.messages.first()
        if last_message:
            return MessageSerializer(last_message, context=self.context).data
        return None

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user:
            participant = obj.participant_details.filter(user=request.user).first()
            if participant and participant.last_read_at:
                return obj.messages.filter(
                    created_at__gt=participant.last_read_at
                ).count()
            return obj.messages.count()
        return 0