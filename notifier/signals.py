import redis
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def announce_new_user(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "gossip", {"type": "user.gossip",
                       "event": "New User",
                       "username": instance.username})


def logged_in(sender, user, request, **kwargs):
    # send to all
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "loggedin", {"type": "user.login",
                     "event": "Message for all: He logged in",
                     "username": user.username})

    # send private to 'z1'
    if user.username == 'admin':
        r = redis.Redis(host='localhost', port=6379, db=0)
        channel_name = r.hget("users", "z1").decode("utf-8")
        if channel_name:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "user_z1", {
                    "type": "private.message",
                    "text": "Hello, Z1!",
                })


user_logged_in.connect(logged_in)
