from django.urls import path
from .views import *

urlpatterns = [

    path(
        'create/',
        TeacherCreateView.as_view()
    ),

    path(
        '',
        TeacherListView.as_view()
    ),

    path(
        '<int:pk>/',
        TeacherDetailView.as_view()
    ),

    path(
        'update/<int:pk>/',
        TeacherUpdateView.as_view()
    ),

    path(
        'delete/<int:pk>/',
        TeacherDeleteView.as_view()
    ),

    path(
        'status/<int:pk>/',
        TeacherStatusView.as_view()
    ),

    path(
        'my-profile/',
        MyTeacherProfileView.as_view()
    ),

    path(
        'my-batches/',
        MyBatchesView.as_view()
    ),
]