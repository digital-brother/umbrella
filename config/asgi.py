import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

import umbrella.notifications.routing
from umbrella.notifications.middleware import TokenAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Local")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": TokenAuthMiddleware(
        URLRouter(
            umbrella.notifications.routing.websocket_urlpatterns
        )
    ),
})
