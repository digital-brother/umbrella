import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import umbrella.notifications.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "umbrella.config")
os.environ.setdefault("DJANGO_CONFIGURATION", "Production")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            umbrella.notifications.routing.websocket_urlpatterns
        )
    ),
})
