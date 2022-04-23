import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from umbrella.notifications.utils import send_message_to_channels_group


class NotificationsConsumer(JsonWebsocketConsumer):
    """
    To send a message from shell:

        import channels

        channel_layer = channels.layers.get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "no_realm", {"type": "chat_message", "message": "Hi"}
        )

    """
    realm = 'no_realm'

    def connect(self):
        # Join room group
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

        # Send message to room group
        send_message_to_channels_group(self.realm, message)

    # Receive message from room group
    def realm_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
