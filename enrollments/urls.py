from django.urls import path

from enrollments.views import *


urlpatterns = [

    path(
        "create/",
        EnrollmentCreateView.as_view()
    ),
    path(
        "",
        EnrollmentListView.as_view(),
        name="enrollment-list"
    ),


    path(
        "<int:pk>/",
        EnrollmentDetailView.as_view(),
        name="enrollment-detail"
    ),


]