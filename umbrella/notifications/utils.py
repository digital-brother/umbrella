from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


def send_message_to_channels_group(group, message):
    async_to_sync(channel_layer.group_send)(
        group, {"type": "realm.message", "message": message}
    )
