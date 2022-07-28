from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker


class TestSetUp(APITestCase):
    ""

    def setUp(_):
        ""
        _.signUpUrl = reverse("signup")
        _.fakedata = Faker()
        _.userData = {
            'email': _.fakedata.email(),
            'username': 'test1',
            "password": "testpass",
        }
        return super(TestSetUp, _).setUp()

    def tearDown(_) -> None:
        return super().tearDown()
