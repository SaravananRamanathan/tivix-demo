from rest_framework.views import APIView
from .serializers import customUserSerializer
from rest_framework.response import Response
from userAccess.models import CustomUser
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()  # loading from .env from root folder.
JWT_SECRET = os.environ.get("JWT_SECRET")


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


class signIn(APIView):
    def post(self, request):
        "Allow users to sign in via api"
        #print(f'recevied from middleware: {request.session["custom_msg"]}')
        email = request.data['email']
        password = request.data['password']

        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found.")
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()  # created date
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256').decode(
            "utf-8")
        response = Response()

        response.set_cookie(key="jwt", value=token, httponly=True)

        response.data = {
            'jwt': token
        }

        return response


class userView(APIView):
    def get(self, request):
        "ping...pong!"
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Not authenticated.")
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithm=['HS256'])
        except jwt.exceptions.ExpiredSignatureError:
            raise AuthenticationFailed("Jwt Token expired")
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed("Incorrect Token Provided")

        user = CustomUser.objects.filter(id=payload['id']).first()
        serializer = customUserSerializer(user)
        return Response(serializer.data)


# todo: need to check if user is logged in to begin with...
class signOut(APIView):
    def post(self, request):
        ""
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'logged out.'
        }
        return response
