"""
ASGI config for telegram project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from chat.chat_middleware import AsyncChatRoomMiddleware 
from channels.sessions import SessionMiddlewareStack
#from channels.middleware import CooieMiddleware 
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter
from chat.routing import websocket_urlpatterns



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram.settings')

application = ProtocolTypeRouter(
    {
        'http':get_asgi_application(),
        'websocket': AllowedHostsOriginValidator(
            SessionMiddlewareStack(
                AsyncChatRoomMiddleware(AuthMiddlewareStack(URLRouter(websocket_urlpatterns)))
            )
        ),
    }
)

#from channels.middleware.base import MiddlewareStack


"""'websocket': MiddlewareStack(
             [
             list of middlewares
             ]
             ,URLRouter(websocket_urlpatterns)
            
"""
                 