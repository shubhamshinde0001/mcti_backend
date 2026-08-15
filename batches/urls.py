from django.urls import path
from .views import *

urlpatterns = [

    path(
        'create/',
        BatchCreateView.as_view()
    ),

    path(
        '',
        BatchListView.as_view()
    ),

    path(
        '<int:pk>/',
        BatchDetailView.as_view()
    ),

    path(
        'update/<int:pk>/',
        BatchUpdateView.as_view()
    ),

    path(
        'delete/<int:pk>/',
        BatchDeleteView.as_view()
    ),

    path(
        'assign-teacher/<int:pk>/',
        AssignTeacherView.as_view()
    ),

    path(
        'status/<int:pk>/',
        BatchStatusView.as_view()
    ),
]