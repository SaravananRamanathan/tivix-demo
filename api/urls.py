from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # test
    path("test", views.test.as_view(),name="test"),
    # signUp
    path("signUp", views.signUp.as_view(), name="signup"),

    # signIn
    path("signIn", views.signIn.as_view(),name="signin"),

    # user
    path("user", views.userView.as_view(),name="user"),

    # signOut
    path("signOut", views.signOut.as_view(),name="signout"),
]
