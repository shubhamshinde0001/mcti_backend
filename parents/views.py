from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import (
    Parent,
    Student
)

from .serializers import (
    ParentSerializer,
    CreateParentSerializer
)

from .permissions import (
    IsHeadAdmin
)

class ParentCreateView(
    generics.CreateAPIView
):

    queryset = Parent.objects.all()

    serializer_class = (
        CreateParentSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]

class ParentListView(
    generics.ListAPIView
):

    queryset = Parent.objects.all()

    serializer_class = (
        ParentSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

class ParentListView(
    generics.ListAPIView
):

    queryset = Parent.objects.all()

    serializer_class = (
        ParentSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

class ParentDetailView(
    generics.RetrieveAPIView
):

    queryset = Parent.objects.all()

    serializer_class = (
        ParentSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

class ParentUpdateView(
    generics.UpdateAPIView
):

    queryset = Parent.objects.all()

    serializer_class = (
        ParentSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]

class ParentDeleteView(
    generics.DestroyAPIView
):

    queryset = Parent.objects.all()

    serializer_class = (
        ParentSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]

class ParentStatusView(
    APIView
):

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]

    def patch(
        self,
        request,
        pk
    ):

        parent = Parent.objects.get(
            id=pk
        )

        parent.status = request.data.get(
            'status'
        )

        parent.save()

        return Response({

            "message":
            "Parent Status Updated"
        })


class MyParentProfileView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        parent = Parent.objects.get(
            user=request.user
        )

        serializer = ParentSerializer(
            parent
        )

        return Response(
            serializer.data
        )

class MyChildrenView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        parent = Parent.objects.get(
            user=request.user
        )

        students = Student.objects.filter(
            parent=parent
        )

        data = []

        for student in students:

            data.append({

                "student_id":
                student.student_id,

                "name":
                f"{student.first_name} {student.last_name}",

                "mobile":
                student.mobile
            })

        return Response(data)
    
from attendance.models import Attendance
from fees.models import StudentFee


class ParentDashboardView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        parent = Parent.objects.get(
            user=request.user
        )

        students = Student.objects.filter(
            parent=parent
        )

        dashboard = []

        for student in students:

            fee = StudentFee.objects.filter(
                enrollment__student=student
            ).first()

            dashboard.append({

                "student":
                student.first_name,

                "total_fee":
                fee.total_fee if fee else 0,

                "paid":
                fee.paid_amount if fee else 0,

                "balance":
                fee.balance_amount if fee else 0
            })

        return Response(dashboard)
    
class ChildAttendanceView(
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

        attendance = Attendance.objects.filter(
            enrollment__student=student
        )

        data = []

        for record in attendance:

            data.append({

                "date": record.date,

                "status": record.status
            })

        return Response(data)
    
