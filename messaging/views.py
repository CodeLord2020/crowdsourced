from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.utils import timezone
from .models import Conversation, Message, ConversationParticipant, MessageRead
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsConversationParticipant, IsMessageSender
from .filters import ConversationFilter, MessageFilter
from django.core.exceptions import PermissionDenied




class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsConversationParticipant]
    filterset_class = ConversationFilter
    ordering = '-updated_at'

    def get_queryset(self):
        return Conversation.objects.filter(
            participants=self.request.user,
            is_active=True
        ).prefetch_related(
            'participants',
            'messages',
            'participant_details'
        )

    def perform_create(self, serializer):
        conversation = serializer.save()
        # Add participants
        participants = self.request.data.get('participants', [])
        participants.append(self.request.user.id)
        for participant_id in set(participants):
            ConversationParticipant.objects.create(
                conversation=conversation,
                user_id=participant_id
            )

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark all messages in conversation as read"""
        conversation = self.get_object()
        participant = conversation.participant_details.get(user=request.user)
        participant.last_read_at = timezone.now()
        participant.save()
        
        # Create MessageRead entries for unread messages
        unread_messages = conversation.messages.exclude(
            read_by=request.user
        )
        MessageRead.objects.bulk_create([
            MessageRead(message=msg, user=request.user)
            for msg in unread_messages
        ])
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """Archive/unarchive conversation"""
        conversation = self.get_object()
        participant = conversation.participant_details.get(user=request.user)
        participant.is_archived = not participant.is_archived
        participant.archived_at = timezone.now() if participant.is_archived else None
        participant.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageSender]
    filterset_class = MessageFilter
    ordering = '-created_at'

    def get_queryset(self):
        return Message.objects.filter(
            conversation__participants=self.request.user,
            conversation__is_active=True
        ).select_related(
            'sender',
            'conversation'
        ).prefetch_related('read_by')

    def perform_create(self, serializer):
        conversation = serializer.validated_data['conversation']
        if not conversation.participants.filter(id=self.request.user.id).exists():
            raise PermissionDenied("You are not a participant in this conversation")
        
        serializer.save(sender=self.request.user)
        
        # Update conversation's updated_at timestamp
        conversation.save()

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()


