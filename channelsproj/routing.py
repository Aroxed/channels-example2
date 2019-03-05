from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from notifier.consumers.default_consumer import DefaultConsumer
from notifier.consumers.single_consumer import SingleConsumer
from channels.auth import AuthMiddlewareStack

application = (ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(URLRouter([
        path("notifications/", DefaultConsumer),
        path("single/", SingleConsumer),
    ]))
}))
