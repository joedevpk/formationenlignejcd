import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning.settings')

django_asgi_app = get_asgi_application()

chat_ws = []
notif_ws = []

try:
    from chat import routing as chat_routing
    chat_ws = chat_routing.websocket_urlpatterns
except Exception:
    pass

try:
    from notifications import routing as notif_routing
    notif_ws = notif_routing.websocket_urlpatterns
except Exception:
    pass

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(chat_ws + notif_ws)
    ),
})
