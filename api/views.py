from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import customUserSerializer
# Create your views here.


class test(APIView):
    "simple api test endpoint"

    def post(self, request):
        "testing api ping..! pong!"
        data = request.data
        response = Response()
        response.data = {
            'message-received': data
        }
        return response


class signUp(APIView):
    def post(self, request):
        "allow users to sign up via api"
        serializer_class = customUserSerializer(data=request.data)
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()
        return Response(serializer_class.data)
