from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from accounts.models import Teacher

from .serializers import (
    TeacherSerializer,
    CreateTeacherSerializer
)

from .permissions import (
    IsHeadAdmin
)

class TeacherCreateView(
    generics.CreateAPIView
):

    queryset = Teacher.objects.all()

    serializer_class = (
        CreateTeacherSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]

class TeacherListView(
    generics.ListAPIView
):

    queryset = Teacher.objects.all()

    serializer_class = (
        TeacherSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

class TeacherDetailView(
    generics.RetrieveAPIView
):

    queryset = Teacher.objects.all()

    serializer_class = (
        TeacherSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

class TeacherUpdateView(
    generics.UpdateAPIView
):

    queryset = Teacher.objects.all()

    serializer_class = (
        TeacherSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]

class TeacherDeleteView(
    generics.DestroyAPIView
):

    queryset = Teacher.objects.all()

    serializer_class = (
        TeacherSerializer
    )

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]

from rest_framework.views import APIView
from rest_framework.response import Response


class TeacherStatusView(
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

        teacher = Teacher.objects.get(
            id=pk
        )

        teacher.status = request.data.get(
            'status'
        )

        teacher.save()

        return Response({
            "message":
            "Teacher Status Updated"
        })
    

class MyTeacherProfileView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        teacher = Teacher.objects.get(
            user=request.user
        )

        serializer = TeacherSerializer(
            teacher
        )

        return Response(
            serializer.data
        )
    
from batches.models import Batch

class MyBatchesView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        teacher = Teacher.objects.get(
            user=request.user
        )

        batches = Batch.objects.filter(
            teacher=teacher
        )

        data = []

        for batch in batches:

            data.append({

                "id": batch.id,

                "batch_name":
                batch.batch_name,

                "course":
                batch.course.course_name,

                "start_date":
                batch.start_date,

                "end_date":
                batch.end_date
            })

        return Response(data)
    

