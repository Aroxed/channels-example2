from channels.generic.websocket import AsyncJsonWebsocketConsumer


class DefaultConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.accept()
        # self.channel_name -- individual unique channel name
        # group_add -- add channel to group
        await self.channel_layer.group_add("gossip", self.channel_name)
        print(f"Added {self.channel_name} channel to gossip")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("gossip", self.channel_name)
        print(f"Removed {self.channel_name} channel to gossip")

    # see signals.py: "gossip", {"type": "user.gossip", ...
    async def user_gossip(self, event):
        await self.send_json(event)
        print(f"Got message {event} at {self.channel_name}")
