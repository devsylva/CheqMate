import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CartConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.cart_id = self.scope['url_route']['kwargs']['cart_id']
        self.room_group_name = f'cart_{self.cart_id}'

        # Join the group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print(f"Connected to {self.room_group_name}")

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"Disconnected from {self.room_group_name}")

    # Receive message from WebSocket
    async def receive(self, text_data):
        print("Message received:", text_data)  # Debugging print
        # Here you can handle the received message (if needed)
        pass

    # Send message to WebSocket
    async def send_cart_sync_update(self, event):
        print(f"Sending sync update: {event['is_synced']}")  # Debugging print
        # Send the cart sync status to WebSocket
        is_synced = event['is_synced']

        # Send the cart_sync_update message to WebSocket
        await self.send(text_data=json.dumps({
            'is_synced': is_synced  # Python's True/False will be sent as true/false
        }))
