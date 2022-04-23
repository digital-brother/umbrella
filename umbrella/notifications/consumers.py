import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from umbrella.notifications.utils import send_message_to_channels_group


class NotificationsConsumer(WebsocketConsumer):
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
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group

        send_message_to_channels_group(self.realm, message)

    # Receive message from room group
    def realm_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
