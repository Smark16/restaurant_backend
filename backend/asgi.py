import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import restaurant.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Initialize the ASGI application
application = get_asgi_application()

# Define the application protocol type router
application = ProtocolTypeRouter({
    'http': application,  # Use the ASGI application we initialized earlier
    'websocket': AuthMiddlewareStack(
        URLRouter(
            restaurant.routing.websocket_urlpatterns
        )
    ),
})
