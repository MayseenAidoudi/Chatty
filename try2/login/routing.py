from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<username_link>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chat/$', consumers.DefaultConsumer.as_asgi()),
]
