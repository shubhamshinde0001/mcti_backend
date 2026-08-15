from django.urls import path
from .views import *

urlpatterns = [

    path(
        'create/',
        ParentCreateView.as_view()
    ),

    path(
        '',
        ParentListView.as_view()
    ),

    path(
        '<int:pk>/',
        ParentDetailView.as_view()
    ),

    path(
        'update/<int:pk>/',
        ParentUpdateView.as_view()
    ),

    path(
        'delete/<int:pk>/',
        ParentDeleteView.as_view()
    ),

    path(
        'status/<int:pk>/',
        ParentStatusView.as_view()
    ),

    path(
        'my-profile/',
        MyParentProfileView.as_view()
    ),

    path(
        'my-children/',
        MyChildrenView.as_view()
    ),

    path(
        'dashboard/',
        ParentDashboardView.as_view()
    ),

    path(
        'attendance/<int:student_id>/',
        ChildAttendanceView.as_view()
    ),
]