from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # test
    path("test", views.test.as_view()),
    # signUp
    path("signUp", views.signUp.as_view()),
]
