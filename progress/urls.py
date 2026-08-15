from django.urls import path

from .views import *

urlpatterns = [

    path(

        "mark-completed/",

        MarkSubjectCompletedView.as_view()
    ),

    path(

        "mark-pending/",

        MarkSubjectPendingView.as_view()
    ),

    path(

        "student/<int:student_id>/",

        StudentProgressView.as_view()
    ),



    path(
    "batch/<int:batch_id>/",
    BatchProgressView.as_view()
),
]