from django.urls import path
from .views import *

urlpatterns = [

    path(
        'register/',
        RegisterView.as_view()
    ),

    path(
        "login/",
        LoginView.as_view()
    ),

    path(
        'users/',
        UserListView.as_view()
    ),

    path(
        "logout/",
        LogoutView.as_view()
    ),
    path(
    'profile/',
    MyProfileView.as_view()
)
]