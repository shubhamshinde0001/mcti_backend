from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated
)

from accounts.models import Student

from .serializers import (
    StudentEnrollmentSerializer,
    StudentSerializer,
    CreateStudentSerializer
)

from .permissions import (
    IsHeadAdmin
)



class StudentCreateView(
    generics.CreateAPIView
):

    queryset = Student.objects.all()

    serializer_class = (
        CreateStudentSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]


class StudentListView(
    generics.ListAPIView
):

    queryset = Student.objects.all()

    serializer_class = (
        StudentSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]


class StudentDetailView(
    generics.RetrieveAPIView
):

    queryset = Student.objects.all()

    serializer_class = (
        StudentSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

class StudentUpdateView(
    generics.UpdateAPIView
):

    queryset = Student.objects.all()

    serializer_class = (
        StudentSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]

class StudentDeleteView(
    generics.DestroyAPIView
):

    queryset = Student.objects.all()

    serializer_class = (
        StudentSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]



from rest_framework.views import APIView
from rest_framework.response import Response


class StudentStatusView(
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

        student = Student.objects.get(
            id=pk
        )

        student.status = request.data.get(
            'status'
        )

        student.save()

        return Response({

            "message":
            "Student Status Updated"
        })
    
class MyProfileView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        student = Student.objects.get(
            user=request.user
        )

        serializer = StudentSerializer(
            student
        )

        return Response(
            serializer.data
        )
    
class MyProfileView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        student = Student.objects.get(
            user=request.user
        )

        serializer = StudentSerializer(
            student
        )

        return Response(
            serializer.data
        )
    
from attendance.models import Attendance
from fees.models import StudentFee
from enrollments.models import Enrollment



class StudentDashboardView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        student = Student.objects.get(
            user=request.user
        )

        enrollments = Enrollment.objects.filter(
            student=student
        )

        total_attendance = Attendance.objects.filter(
            enrollment__student=student
        ).count()

        present = Attendance.objects.filter(
            enrollment__student=student,
            status='PRESENT'
        ).count()

        attendance_percentage = 0

        if total_attendance > 0:

            attendance_percentage = (
                present /
                total_attendance
            ) * 100

        fee = StudentFee.objects.filter(
            enrollment__student=student
        ).first()

        course_serializer = StudentEnrollmentSerializer(
        enrollments,
        many=True
)

        return Response({

        "student_name": student.first_name,

        "attendance_percentage": round(
            attendance_percentage,
            2
        ),

        "total_fee": fee.total_fee if fee else 0,

        "paid_amount": fee.paid_amount if fee else 0,

        "balance_amount": fee.balance_amount if fee else 0,

        "active_enrollments": enrollments.count(),

        "courses": course_serializer.data
    })


from enrollments.models import Enrollment
from .serializers import StudentEnrollmentSerializer


class MyCoursesView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        student = Student.objects.get(
            user=request.user
        )

        enrollments = Enrollment.objects.filter(
            student=student
        ).select_related(
            "batch",
            "batch__course",
            "batch__teacher"
        )

        serializer = StudentEnrollmentSerializer(
            enrollments,
            many=True
        )

        return Response(serializer.data)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import Student
from enrollments.models import Enrollment

from .serializers import (
    StudentCourseDashboardSerializer
)


# class CurrentCourseView(APIView):

#     permission_classes = [
#         IsAuthenticated
#     ]

#     def get(self, request):

#         student = Student.objects.get(
#             user=request.user
#         )

#         enrollment = Enrollment.objects.select_related(

#             "batch",

#             "batch__course",

#             "batch__teacher",

#             "batch__teacher__user"

#         ).get(

#             student=student,

#             status="ACTIVE"

#         )

#         serializer = StudentCourseDashboardSerializer(
#             enrollment
#         )

#         return Response(
#             serializer.data
#         )


class CurrentCourseView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        print("=" * 60)
        print("Logged User ID :", request.user.id)
        print("Username       :", request.user.username)
        print("Role           :", request.user.role)
        print("Authenticated  :", request.user.is_authenticated)

        print(
            Student.objects.values(
                "id",
                "user_id",
                "first_name"
            )
        )

        student = Student.objects.get(user=request.user)

        enrollment = Enrollment.objects.select_related(
            "batch",
            "batch__course",
            "batch__teacher",
            "batch__teacher__user"
        ).get(
            student=student,
            status="ACTIVE"
        )

        serializer = StudentCourseDashboardSerializer(enrollment)

        return Response(serializer.data)