from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # signUp
    path("test", views.test.as_view()),
]

