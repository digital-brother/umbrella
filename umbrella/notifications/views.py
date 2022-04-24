from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from umbrella.notifications.utils import send_message_to_channels_group


class SendNotificationView(GenericAPIView):
    def post(self, request):
        # TODO: validation
        message = request.data['message']
        realm = request.user.realm

        send_message_to_channels_group(realm, message)

        return Response({
            "group": realm,
            "message": message,
        })
