import pytest
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator

from umbrella.notifications.consumers import NotificationsConsumer
from umbrella.notifications.middleware import TokenAuthMiddleware
from umbrella.notifications.utils import send_message_to_channels_group

pytestmark = [pytest.mark.asyncio, pytest.mark.django_db(transaction=True)]


async def test_notifications_consumer(user):
    url = f'?token={user.auth_token}'
    communicator = WebsocketCommunicator(TokenAuthMiddleware(NotificationsConsumer.as_asgi()), url)

    connected, subprotocol = await communicator.connect()
    assert connected

    # Test sending text
    test_message = 'test_message'
    await sync_to_async(send_message_to_channels_group)(user.realm, test_message)
    response = await communicator.receive_json_from()
    assert response['message'] == test_message

    # Close
    await communicator.disconnect()
