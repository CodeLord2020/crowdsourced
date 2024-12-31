
from rest_framework import permissions


class IsConversationParticipant(permissions.BasePermission):
    """Permission to only allow participants of a conversation to access it"""
    def has_object_permission(self, request, view, obj):
        return obj.participants.filter(id=request.user.id).exists()


class IsMessageSender(permissions.BasePermission):
    """Permission to only allow message sender to edit/delete their messages"""
    def has_object_permission(self, request, view, obj):
        if request.method in ['DELETE', 'PATCH', 'PUT']:
            return obj.sender == request.user
        return True