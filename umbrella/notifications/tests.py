import pytest
from channels.testing import WebsocketCommunicator

from umbrella.notifications.consumers import NotificationsConsumer
from umbrella.notifications.middleware import TokenAuthMiddleware

pytestmark = [pytest.mark.asyncio, pytest.mark.django_db(transaction=True)]


async def test_notifications_consumer(user):
    url = f'?token={user.auth_token}'
    communicator = WebsocketCommunicator(TokenAuthMiddleware(NotificationsConsumer.as_asgi()), url)
    connected, subprotocol = await communicator.connect()
    assert connected

    # Test sending text
    data = {'message': 'hello'}
    await communicator.send_json_to(data)
    response = await communicator.receive_json_from()
    assert response['message'] == data['message']

    # Close
    await communicator.disconnect()
