from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


class NotificationsConsumer(JsonWebsocketConsumer):
    """
    Once the user connects to the endpoint, he is added to the channel group named the same as his realm.
    To send a message to all connected users belonging a specific realm, use send_message_to_channels_group().
    """
    def connect(self):
        self.accept()
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            self.send_json({'error': 'Incorrect authentication credentials.'})
            self.close()
            return

        # Join realm group
        self.realm = self.user.realm
        async_to_sync(self.channel_layer.group_add)(
            self.realm,
            self.channel_name
        )

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.realm,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive_json(self, content, **kwargs):
        message = content.get('message')

        # Send message to room group
        self.send_message_to_channels_group(self.realm, message)

    # Receive message from room group
    def realm_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send_json({
            'message': message,
            'user': self.user.username,
        })

    @classmethod
    def send_message_to_channels_group(cls, group, message):
        async_to_sync(channel_layer.group_send)(
            group, {"type": "realm.message", "message": message}
        )
