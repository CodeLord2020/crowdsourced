
from django_filters import rest_framework as filters
from .models import Conversation, Message
from django.db import models


class ConversationFilter(filters.FilterSet):
    """Filter set for conversations"""
    unread_only = filters.BooleanFilter(method='filter_unread')
    archived = filters.BooleanFilter(method='filter_archived')
    participant = filters.UUIDFilter(method='filter_participant')
    before = filters.DateTimeFilter(field_name='updated_at', lookup_expr='lt')
    after = filters.DateTimeFilter(field_name='updated_at', lookup_expr='gt')

    class Meta:
        model = Conversation
        fields = ['unread_only', 'archived', 'participant', 'before', 'after']

    def filter_unread(self, queryset, name, value):
        if not value:
            return queryset
        user = self.request.user
        return queryset.filter(
            participant_details__user=user,
            messages__created_at__gt=models.F('participant_details__last_read_at')
        ).distinct()

    def filter_archived(self, queryset, name, value):
        user = self.request.user
        return queryset.filter(
            participant_details__user=user,
            participant_details__is_archived=value
        )

    def filter_participant(self, queryset, name, value):
        return queryset.filter(participants__id=value)