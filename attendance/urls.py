from django.urls import path
from .views import *

urlpatterns = [

    path(
        'mark/',
        MarkAttendanceView.as_view()
    ),

    path(
        '',
        AttendanceListView.as_view()
    ),

    path(
        'update/<int:pk>/',
        AttendanceUpdateView.as_view()
    ),

    path(
        'delete/<int:pk>/',
        AttendanceDeleteView.as_view()
    ),

    path(
        'batch/<int:batch_id>/',
        BatchAttendanceView.as_view()
    ),

    path(
        'percentage/<int:enrollment_id>/',
        StudentAttendancePercentage.as_view()
    ),

    path(
        'monthly/<int:student_id>/<int:month>/<int:year>/',
        MonthlyAttendanceReport.as_view()
    ),
]