from django.urls import path
from .views import *

urlpatterns = [

    # path(
    #     'create/',
    #     CourseCreateView.as_view(),
    #     name='create-course'
    # ),

    # path(
    #     '',
    #     CourseListView.as_view(),
    #     name='course-list'
    # ),

    # path(
    #     '<int:pk>/',
    #     CourseDetailView.as_view(),
    #     name='course-detail'
    # ),

    # path(
    #     'update/<int:pk>/',
    #     CourseUpdateView.as_view(),
    #     name='update-course'
    # ),

    # path(
    #     'delete/<int:pk>/',
    #     CourseDeleteView.as_view(),
    #     name='delete-course'
    # ),

    # path(
    #     'status/<int:pk>/',
    #     CourseStatusView.as_view(),
    #     name='course-status'
    # ),


        path(
        "",
        CourseListView.as_view()
    ),

    path(
        "<int:pk>/",
        CourseDetailView.as_view()
    ),

    path(
        "create/",
        CourseCreateView.as_view()
    ),

    path(
        "<int:pk>/update/",
        CourseUpdateView.as_view()
    ),

    path(
        "<int:pk>/delete/",
        CourseDeleteView.as_view()
    ),

    path(
        "<int:pk>/status/",
        CourseStatusView.as_view()
    ),

    # Subject APIs

    path(
        "subjects/",
        SubjectListView.as_view()
    ),

    path(
        "subjects/create/",
        SubjectCreateView.as_view()
    ),

    path(
        "subjects/<int:pk>/",
        SubjectDetailView.as_view()
    ),

    path(
        "subjects/<int:pk>/update/",
        SubjectUpdateView.as_view()
    ),

    path(
        "subjects/<int:pk>/delete/",
        SubjectDeleteView.as_view()
    ),

    path(
        "<int:pk>/subjects/",
        CourseSubjectsView.as_view()
    ),
]