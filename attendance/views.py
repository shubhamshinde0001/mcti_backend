from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Attendance
from .serializers import AttendanceSerializer
from .permissions import IsTeacherOrHead

class MarkAttendanceView(
    generics.CreateAPIView
):

    queryset = Attendance.objects.all()

    serializer_class = AttendanceSerializer

    permission_classes = [
        IsAuthenticated,
        IsTeacherOrHead
    ]

class AttendanceListView(
    generics.ListAPIView
):

    queryset = Attendance.objects.all()

    serializer_class = AttendanceSerializer

    permission_classes = [
        IsAuthenticated
    ]

class AttendanceUpdateView(
    generics.UpdateAPIView
):

    queryset = Attendance.objects.all()

    serializer_class = AttendanceSerializer

    permission_classes = [
        IsAuthenticated,
        IsTeacherOrHead
    ]

from accounts.permissions import IsHeadAdmin


class AttendanceDeleteView(
    generics.DestroyAPIView
):

    queryset = Attendance.objects.all()

    serializer_class = AttendanceSerializer

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]

from batches.models import Batch
from enrollments.models import Enrollment
from rest_framework.views import APIView
from rest_framework.response import Response

class BatchAttendanceView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsTeacherOrHead
    ]

    def get(self, request, batch_id):

        enrollments = Enrollment.objects.filter(
            batch_id=batch_id,
            status='ACTIVE'
        )

        data = []

        for enrollment in enrollments:

            data.append({

                "enrollment_id":
                enrollment.id,

                "student_name":
                enrollment.student.user.username,

                "student_id":
                enrollment.student.id
            })

        return Response(data)
    

from django.db.models import Count

class StudentAttendancePercentage(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
        enrollment_id
    ):

        total = Attendance.objects.filter(
            enrollment_id=enrollment_id
        ).count()

        present = Attendance.objects.filter(
            enrollment_id=enrollment_id,
            status='PRESENT'
        ).count()

        percentage = 0

        if total > 0:

            percentage = (
                present / total
            ) * 100

        return Response({

            "total_classes": total,

            "present": present,

            "attendance_percentage":
            round(
                percentage,
                2
            )
        })
    
class MonthlyAttendanceReport(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
        student_id,
        month,
        year
    ):

        records = Attendance.objects.filter(
            enrollment__student_id=student_id,
            date__month=month,
            date__year=year
        )

        serializer = AttendanceSerializer(
            records,
            many=True
        )

        return Response(
            serializer.data
        )