import pytest
from channels.testing import WebsocketCommunicator

from umbrella.notifications.consumers import NotificationsConsumer


@pytest.mark.asyncio
async def test_notifications_consumer():
    communicator = WebsocketCommunicator(NotificationsConsumer.as_asgi(), "")
    connected, subprotocol = await communicator.connect()
    assert connected

    # Test sending text
    data = {'message': 'hello'}
    await communicator.send_json_to(data)
    response = await communicator.receive_json_from()
    assert response == data

    # Close
    await communicator.disconnect()
