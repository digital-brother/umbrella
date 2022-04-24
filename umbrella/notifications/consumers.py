from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from umbrella.notifications.utils import send_message_to_channels_group


class NotificationsConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        
        if self.user.is_authenticated:
            # Join realm group
            self.realm = self.user.realm
            async_to_sync(self.channel_layer.group_add)(
                self.realm,
                self.channel_name
            )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.realm,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive_json(self, content, **kwargs):
        message = content['message']

        if not self.user.is_authenticated:
            self.send_json({'error': 'Incorrect authentication credentials.'})
            return

        # Send message to room group
        send_message_to_channels_group(self.realm, message)

    # Receive message from room group
    def realm_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send_json({
            'message': message,
            'user': self.user.username,
        })
