from rest_framework.response import Response
from rest_framework.views import APIView


class AddFileView(APIView):
    def get(self, request):
        return Response('Ok')
