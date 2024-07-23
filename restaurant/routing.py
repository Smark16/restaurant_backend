from . import consumers
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/socket-server/(?P<user_id>\w+)/$', consumers.ChatConsumer.as_asgi())
]
