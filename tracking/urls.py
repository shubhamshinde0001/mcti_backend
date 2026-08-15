from django.urls import path
from .views import *

urlpatterns = [

    path(
        'check-in/',
        StudentCheckInView.as_view()
    ),

    path(
        'check-out/',
        StudentCheckOutView.as_view()
    ),

    path(
        'history/<int:student_id>/',
        StudentTrackingHistoryView.as_view()
    ),

    path(
        'inside/',
        StudentsInsideView.as_view()
    ),

    path(
        'daily-report/',
        DailyTrackingReportView.as_view()
    ),

    path(
        'child/<int:student_id>/',
        ChildTrackingView.as_view()
    ),
]