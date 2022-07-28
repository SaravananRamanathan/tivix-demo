from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    # test
    path("test", views.test.as_view(), name="test"),
    # signUp
    path("signUp", views.signUp.as_view(), name="signup"),

    # signIn
    path("signIn", views.signIn.as_view(), name="signin"),

    # user
    path("user", views.userView.as_view(), name="user"),

    # signOut
    path("signOut", views.signOut.as_view(), name="signout"),

    # get all budgets -- just returning a list of all budget names a user has.
    path("getAllBudgets/", views.getAllBudgets.as_view(), name="getAllBudgets"),

    # get the budget details based on id sent, if the user has access to that id.
    re_path("getBudgetDetailsById/(?P<id>\w+)$",
            views.getBudgetDetailsById.as_view()),
]
