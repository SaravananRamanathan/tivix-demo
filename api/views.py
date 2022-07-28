from django.db import IntegrityError
from rest_framework.views import APIView
from .serializers import budgetSerializer, customUserSerializer, itemSerializer, shareSerializer
from rest_framework.response import Response
from userAccess.models import CustomUser
from rest_framework.exceptions import AuthenticationFailed, NotFound, NotAcceptable
from django.core.exceptions import BadRequest
import jwt
import datetime
import os
from dotenv import load_dotenv
from rest_framework import generics
from .models import Budget, share as SHARE
from rest_framework import status
from django.db.models.deletion import ProtectedError
from rest_framework.settings import APISettings, DEFAULTS, IMPORT_STRINGS

load_dotenv()  # loading from .env from root folder.
JWT_SECRET = os.environ.get("JWT_SECRET")


def autheticator(token):
    "token validation."
    if not token:
        raise AuthenticationFailed("Not authenticated.")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithm=['HS256'])
    except jwt.exceptions.ExpiredSignatureError:
        raise AuthenticationFailed("Jwt Token expired")
    except jwt.exceptions.InvalidSignatureError:
        raise AuthenticationFailed("Incorrect Token Provided")

    return payload


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

        payload = autheticator(token)

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


# custom list model mixin:
class ListModelMixin2:
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        response = Response()
        # print(f"id= {self.payload['id']}") #getting user id --test ok.

        print(SHARE.objects.filter(shared_with_id=self.payload['id']))
        sharedata = SHARE.objects.filter(shared_with_id=self.payload['id'])
        sharedFrom = dict()

        j = 1
        for i in sharedata:
            budgetdict = dict()
            print(i.budget_id)
            budgetdata = Budget.objects.filter(id=i.budget_id).first()
            print(budgetdata.name)
            tempuser = CustomUser.objects.filter(id=budgetdata.user_id).first()
            budgetdict["id"] = budgetdata.id
            budgetdict["name"] = budgetdata.name
            sharedFrom[tempuser.email] = budgetdict

        response.data = {
            "self-Budgets": serializer.data,
            "Shared-from": sharedFrom
        }

        """response.data = {
            "Budget": serializer.data
        }"""
        return Response(response.data)


class getAllBudgets(ListModelMixin2, generics.ListAPIView):
    serializer_class = budgetSerializer

    def get_queryset(self):
        token = self.request.COOKIES.get('jwt')

        self.payload = autheticator(token)

        users = CustomUser.objects.filter(id=self.payload['id']).first()
        serializer = customUserSerializer(users)
        budget = Budget.objects.filter(user_id=serializer.data['id'])
        print(budget)

        return budget  # Product.objects.get(user=user)


# custom list model mixin:
class ListModelMixin:
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        response = Response()
        print(f"id= {self.kwargs['id']}")

        print(SHARE.objects.filter(budget_id=self.kwargs['id']))
        sharedata = SHARE.objects.filter(budget_id=self.kwargs['id'])
        sharedWith = dict()
        j = 1
        for i in sharedata:
            print(i.shared_with_id)
            tempuser = CustomUser.objects.filter(id=i.shared_with_id).first()
            print(tempuser.email)
            sharedWith["email{}".format(j)] = tempuser.email
            j += 1
        response.data = {
            "Budget": serializer.data,
            "Shared-With": sharedWith
        }
        return Response(response.data)


class getBudgetDetailsById(ListModelMixin, generics.ListCreateAPIView):
    serializer_class = itemSerializer

    def get_queryset(self):
        token = self.request.COOKIES.get('jwt')

        payload = autheticator(token)

        users = CustomUser.objects.filter(id=payload['id']).first()
        # print(users) #test ok
        serializer = customUserSerializer(users)
        # print(serializer.data['id'])  #test ok
        # print(self.kwargs['id'])   #test ok

        budget = Budget.objects.filter(
            user_id=serializer.data['id'], id=self.kwargs['id'])
        if not budget:
            ""
            # in here need to check if they have shared access from other users
            # before rejecting their request.
            shared = SHARE.objects.filter(
                shared_with_id=serializer.data["id"], budget_id=self.kwargs['id']).first()
            print(shared)  # test ok.
            if not shared:
                raise NotFound(
                    "You dont have access to any budget with that id.")
            else:
                budget = Budget.objects.filter(id=self.kwargs['id'])
                print(budget)  # test ok.
        # print(budget) #test ok!..!
        print(budget[0].item_set.all())
        return budget[0].item_set.all()


# deleteBudgetById
# my custom destroy mixin.
class DestroyModelMixin(object):
    """
    Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError as e:
            return Response(status=status.HTTP_423_LOCKED, data={'detail': str(e)})
        # return Response(status=status.HTTP_204_NO_CONTENT) #this is django default...
        # custom Response return on deletion.
        return Response({'message': 'Deleted Successfully'})

    def perform_destroy(self, instance):
        instance.delete()


class deleteBudgetById(DestroyModelMixin, generics.DestroyAPIView):
    serializer_class = budgetSerializer
    #lookup_url_kwarg = pk
    lookup_field = "id"

    def get_queryset(self):
        token = self.request.COOKIES.get('jwt')
        payload = autheticator(token)
        users = CustomUser.objects.filter(id=payload['id']).first()
        # print(users) #test ok
        serializer = customUserSerializer(users)
        # print(serializer.data['id'])  #test ok
        # print(self.kwargs['id'])   #test ok
        budget = Budget.objects.filter(
            user_id=serializer.data['id'], id=self.kwargs['id'])
        print(budget)
        if not budget:
            ""
            raise NotFound("You dont have access to any budget with that id.")
        # print(product) #test ok!
        # product.delete()
        response = Response()
        response.content = budget
        response.data = {
            'message': 'Deleted successfully.'
        }
        # return response #test ok.
        return budget


# sharing:
"""#scarpping it off as wrong choice for now.
class share(APIView):
    def post(self, request):
        "allow users to share budget with each other via email-id"
        serializer_class = shareSerializer(data=request.data)
        serializer_class.is_valid(raise_exception=True)
        serializer_class.save()
        return Response(serializer_class.data)
"""

# custom create model mixin
api_settings = APISettings(None, DEFAULTS, IMPORT_STRINGS)


class CreateModelMixin:
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        print(request.data)
        token = self.request.COOKIES.get('jwt')
        payload = autheticator(token)

        # finding budget object via id provided.
        users = CustomUser.objects.filter(id=payload['id']).first()
        serializer = customUserSerializer(users)
        budget = Budget.objects.filter(
            user_id=serializer.data['id'], id=request.data['budget'])
        if not budget:
            ""
            raise NotFound("You dont have access to any budget with that id.")
        print(budget[0].pk)
        # set the budget object based on id entered by user.
        request.data['budget'] = budget[0].pk

        # finding id via email provided.
        email = CustomUser.objects.filter(email=request.data["shared_with"])
        if not email:
            raise NotFound("No user with that email provided")
        print(email[0].pk)
        request.data['shared_with'] = email[0].pk

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        # creating a custom response to show to user.
        response = Response()
        response.data = {
            'message': 'added successfully',
            'shared_with': email[0].email
        }
        headers = self.get_success_headers(serializer.data)

        return Response(response.data, status=status.HTTP_201_CREATED, headers=headers)
        # return response

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class share(CreateModelMixin, generics.CreateAPIView):
    "All done via custom model mixin"
    serializer_class = shareSerializer
    # lookup_field="id"


# custom list model mixin:
class ListModelMixin3:
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        print("starting test")
        #budgetdata = dict()
        #userdata = dict()
        ans = dict()
        k = 1
        l = 1
        for i in serializer.data:
            # print(i)
            budgetdata = dict()
            print(f'id= {i.get("id")}')
            budgetdata["id"] = i.get("id")
            budgetdata["name"] = i.get("name")
            tempshare = SHARE.objects.filter(budget_id=i.get("id"))
            if tempshare:
                userdata = dict()
                for j in tempshare:

                    print(j.shared_with_id)
                    tempuser = CustomUser.objects.filter(
                        id=j.shared_with_id).first()
                    if tempuser:
                        print(tempuser.email)
                        userdata["{}".format(k)] = tempuser.email
                        k += 1
                #budgetdata["{}".format(i.get("id"))] = userdata
                budgetdata["shared-to"] = userdata

                ans["{}".format(l)] = budgetdata
                l += 1
                k = 1  # reset counter for emails.
        """response = Response()
        # print(f"id= {self.payload['id']}") #getting user id --test ok.

        print(SHARE.objects.filter(shared_with_id=self.payload['id']))
        sharedata = SHARE.objects.filter(shared_with_id=self.payload['id'])
        sharedFrom = dict()

        j = 1
        for i in sharedata:
            budgetdict = dict()
            print(i.budget_id)
            budgetdata = Budget.objects.filter(id=i.budget_id).first()
            print(budgetdata.name)
            tempuser = CustomUser.objects.filter(id=budgetdata.user_id).first()
            budgetdict["id"] = budgetdata.id
            budgetdict["name"] = budgetdata.name
            sharedFrom[tempuser.email] = budgetdict

        response.data = {
            "self-Budgets": serializer.data,
            "Shared-from": sharedFrom
        }"""

        """response.data = {
            "Budget": serializer.data
        }"""
        # return Response(response.data)
        return Response(ans)


class myshare(ListModelMixin3, generics.ListAPIView):
    serializer_class = budgetSerializer

    def get_queryset(self):
        token = self.request.COOKIES.get('jwt')

        self.payload = autheticator(token)

        users = CustomUser.objects.filter(id=self.payload['id']).first()
        serializer = customUserSerializer(users)
        budget = Budget.objects.filter(user_id=serializer.data['id'])
        print(budget)

        return budget  # Product.objects.get(user=user)


# unshare
class unshare(APIView):
    def post(self, request):
        "stop sharing the bedget to specific users"
        token = request.COOKIES.get('jwt')

        payload = autheticator(token)

        user = CustomUser.objects.filter(id=payload['id']).first()
        serializer = customUserSerializer(user)
        budget = Budget.objects.filter(
            user_id=serializer.data['id'], id=request.data["budget"])
        if not budget:
            raise NotFound("no match with that id found on your budgets")
        else:
            print("budget exists")
            emailcheck = CustomUser.objects.filter(
                email=request.data["shared_with"]).first()
            if emailcheck:
                print(emailcheck)
                request.data["shared_with"] = emailcheck.id
        #serializer_class = shareSerializer()
        tempshare = SHARE.objects.filter(
            budget=request.data["budget"], shared_with=request.data["shared_with"])
        if not tempshare:
            ""
            raise NotFound(
                "no match with that email and id found on your budgets")
        else:
            "valid case"
            tempshare.delete()

        # serializer_class.is_valid(raise_exception=True)
        # serializer_class.delete()
        response = Response()
        response.data = {
            "msg": "stoppped sharing successfully"
        }
        return response


# custom create model mixin
#api_settings = APISettings(None, DEFAULTS, IMPORT_STRINGS)


class CreateModelMixin1:
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        print(request.data)
        token = self.request.COOKIES.get('jwt')
        payload = autheticator(token)

        # finding budget object via id provided.
        users = CustomUser.objects.filter(id=payload['id']).first()
        serializer = customUserSerializer(users)

        # adding user id to request.data
        request.data['user'] = users.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        # creating a custom response to show to user.
        response = Response()
        response.data = {
            'message': 'budget created successfully',
            'budget name': request.data["name"]
        }
        headers = self.get_success_headers(serializer.data)

        return Response(response.data, status=status.HTTP_201_CREATED, headers=headers)
        # return response

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class addBudget(CreateModelMixin1, generics.CreateAPIView):
    "All done via custom model mixin"
    serializer_class = budgetSerializer
    # lookup_field="id"


# custom create model mixin
#api_settings = APISettings(None, DEFAULTS, IMPORT_STRINGS)
class CreateModelMixin2:
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        print(request.data)
        token = self.request.COOKIES.get('jwt')
        payload = autheticator(token)

        # finding budget object via id provided.
        users = CustomUser.objects.filter(id=payload['id']).first()
        serializer = customUserSerializer(users)

        # finding if the user has access to the budget
        budget = Budget.objects.filter(
            id=request.data["budget"], user_id=serializer.data["id"])
        if not budget:
            raise NotFound("the entered id is not found on your budgets")
        if request.data["type"] == "income":
            request.data["type"] = 1
        elif request.data["type"] == "expense":
            request.data["type"] = 2
        else:
            raise BadRequest("type format specified is invalid.")

        # sample
        # "itemName": "salary",
        # "type": "income",
        # "income": "1000",
        # "expense": null,
        # "budget_id": 6

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.perform_create(serializer)
        except IntegrityError:
            raise NotAcceptable("integrity compromised")

        # creating a custom response to show to user.
        response = Response()
        response.data = {
            'message': 'budget items added successfully',
        }
        headers = self.get_success_headers(serializer.data)

        return Response(response.data, status=status.HTTP_201_CREATED, headers=headers)
        # return response

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class addBudgetItemById(CreateModelMixin2, generics.CreateAPIView):
    "All done via custom model mixin"
    serializer_class = itemSerializer
    # lookup_field="id"
