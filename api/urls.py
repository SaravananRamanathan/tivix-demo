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
            views.getBudgetDetailsById.as_view(), name="getBudgetDetailsById"),

    # delete budget based on id sent, if the user has access to that id.
    re_path("deleteBudgetById/(?P<id>\w+)$",
            views.deleteBudgetById.as_view(), name="deleteBudgetById"),

    # share
    path("share", views.share.as_view(), name="share"),

    # unshare
    path("unshare", views.unshare.as_view(), name="unshare"),

    # myshare
    re_path("myshare", views.myshare.as_view(), name="myshare"),

    # addBudget
    path("addBudget", views.addBudget.as_view(), name="addbudget"),

    # addBudgetItemById
    path("addBudgetItemById", views.addBudget.as_view(), name="addBudgetItemById"),
]
