from rest_framework.generics import ListAPIView
from rest_framework.response import Response


class NotificationsListView(ListAPIView):
    def get(self, request, **kwargs):
        return Response('Ok')
