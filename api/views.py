from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


class test(APIView):
    def post(self, request):
        "testing api ping..! pong!"
        data = request.data
        response = Response()
        response.data = {
            'message-received': data
        }
        return response
