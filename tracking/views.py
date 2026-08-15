from django.shortcuts import render

# Create your views here.
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated
)

from .models import StudentTracking

from accounts.models import Student

from .serializers import (
    StudentTrackingSerializer
)

from .permissions import (
    IsTeacherOrHead
)



class StudentCheckInView(
    APIView
):

    permission_classes = [
        IsAuthenticated,
        IsTeacherOrHead
    ]

    def post(
        self,
        request
    ):

        student_id = request.data.get(
            'student_id'
        )

        student = Student.objects.get(
            id=student_id
        )

        today = timezone.now().date()

        existing = StudentTracking.objects.filter(
            student=student,
            date=today,
            check_out__isnull=True
        ).first()

        if existing:

            return Response({

                "error":
                "Student already checked in."
            }, status=400)

        tracking = StudentTracking.objects.create(

            student=student,

            date=today,

            check_in=timezone.now(),

            status='IN'
        )

        return Response({

            "message":
            "Check-In Successful",

            "tracking_id":
            tracking.id
        })
    

class StudentCheckOutView(
    APIView
):

    permission_classes = [
        IsAuthenticated,
        IsTeacherOrHead
    ]

    def post(
        self,
        request
    ):

        student_id = request.data.get(
            'student_id'
        )

        student = Student.objects.get(
            id=student_id
        )

        today = timezone.now().date()

        tracking = StudentTracking.objects.filter(

            student=student,

            date=today,

            check_out__isnull=True

        ).first()

        if not tracking:

            return Response({

                "error":
                "No active check-in found."

            }, status=400)

        tracking.check_out = timezone.now()

        tracking.status = 'OUT'

        tracking.save()

        return Response({

            "message":
            "Check-Out Successful"
        })
    

class StudentTrackingHistoryView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
        student_id
    ):

        records = StudentTracking.objects.filter(
            student_id=student_id
        )

        serializer = StudentTrackingSerializer(
            records,
            many=True
        )

        return Response(
            serializer.data
        )
    

class StudentsInsideView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        today = timezone.now().date()

        records = StudentTracking.objects.filter(

            date=today,

            status='IN',

            check_out__isnull=True

        )

        serializer = StudentTrackingSerializer(
            records,
            many=True
        )

        return Response(
            serializer.data
        )
    
from accounts.models import Parent

class ChildTrackingView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
        student_id
    ):

        parent = Parent.objects.get(
            user=request.user
        )

        student = Student.objects.get(
            id=student_id,
            parent=parent
        )

        records = StudentTracking.objects.filter(
            student=student
        )

        serializer = StudentTrackingSerializer(
            records,
            many=True
        )

        return Response(
            serializer.data
        )
    
    
    
class DailyTrackingReportView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        today = timezone.now().date()

        records = StudentTracking.objects.filter(
            date=today
        )

        serializer = StudentTrackingSerializer(
            records,
            many=True
        )

        return Response(
            serializer.data
        )
    
