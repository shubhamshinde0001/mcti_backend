from django.urls import path

from .views import *



urlpatterns = [

    path(
        'create/',
        AdmissionCreateView.as_view()
    ),
]