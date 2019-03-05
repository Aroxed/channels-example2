import redis
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class SingleConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    async def connect(self):
        await self.accept()
        print(self.scope)
        if 'user' in self.scope and not self.scope['user'].is_anonymous:
            the_user = self.scope['user']
            self.redis.hset("users", the_user.username, self.channel_name)
            await self.channel_layer.group_add("user_{}".format(the_user.username), self.channel_name)
        await self.channel_layer.group_add("loggedin", self.channel_name)
        print(f"Added {self.channel_name} channel to loggedin")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("loggedin", self.channel_name)
        if 'user' in self.scope and not self.scope['user'].is_anonymous:
            the_user = self.scope['user']
            await self.channel_layer.group_discard("user_{}".format(the_user.username), self.channel_name)

        if 'user' in self.scope:
            self.redis.hdel("users", self.scope['user'].username)
        print(f"Removed {self.channel_name} channel to loggedin")

    async def user_login(self, event):
        await self.send_json(event)
        print(f"Got message {event} at {self.channel_name}")

    async def private_message(self, event):
        await self.send_json(event)
        print(f"Got message {event} at {self.channel_name}")
