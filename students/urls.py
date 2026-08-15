from django.urls import path

from .views import *



urlpatterns = [

    path(
        'create/',
        StudentCreateView.as_view()
    ),

    path(
        '',
        StudentListView.as_view()
    ),

    path(
        '<int:pk>/',
        StudentDetailView.as_view()
    ),

    path(
        'update/<int:pk>/',
        StudentUpdateView.as_view()
    ),

    path(
        'delete/<int:pk>/',
        StudentDeleteView.as_view()
    ),

    path(
        'status/<int:pk>/',
        StudentStatusView.as_view()
    ),

    path(
        'my-profile/',
        MyProfileView.as_view()
    ),

    path(
        'dashboard/',
        StudentDashboardView.as_view()
    ),

    path(
    "my-courses/",
    MyCoursesView.as_view(),
    name="my-courses"
),
]


from .views import CurrentCourseView

urlpatterns += [

    path(

        "current-course/",

        CurrentCourseView.as_view(),

        name="current-course"

    ),
]