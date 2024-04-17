from django.urls import path
from . import consumers

# websocket_urlpatterns: A list of URL patterns that are used to route WebSocket connections to the appropriate consumer.
websocket_urlpatterns = [
    path('ws/session/<str:session_id>/', consumers.ChatConsumer.as_asgi())
]