import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning.settings')

django_asgi_app = get_asgi_application()

# IMPORT SAFE (évite crash Render)
try:
    import chat.routing
    chat_ws = chat.routing.websocket_urlpatterns
except Exception:
    chat_ws = []

try:
    import notifications.routing
    notif_ws = notifications.routing.websocket_urlpatterns
except Exception:
    notif_ws = []

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(chat_ws + notif_ws)
    ),
})
