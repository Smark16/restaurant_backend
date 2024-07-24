from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/customer/(?P<user_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/admin/(?P<user_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
]

