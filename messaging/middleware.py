from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from jwt import decode as jwt_decode
from jwt.exceptions import InvalidTokenError



User = get_user_model()

class WebSocketAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        try:
            # Get token from query string
            query_string = scope.get('query_string', b'').decode()
            token = dict(pair.split('=') for pair in query_string.split('&')).get('token', '')
            
            if token:
                # Validate token and get user
                user = await self.get_user_from_token(token)
                scope['user'] = user
            else:
                scope['user'] = AnonymousUser()
                
        except (ValueError, InvalidTokenError):
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)