from rest_framework import generics
from .models import Course
from .serializers import CourseSerializer
from .permissions import IsHeadAdmin
from rest_framework.permissions import IsAuthenticated


class CourseCreateView(
    generics.CreateAPIView
):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]


class CourseListView(
    generics.ListAPIView
):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    permission_classes = [
        IsAuthenticated
    ]


class CourseDetailView(
    generics.RetrieveAPIView
):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    permission_classes = [
        IsAuthenticated
    ]


class CourseUpdateView(
    generics.UpdateAPIView
):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]


class CourseDeleteView(
    generics.DestroyAPIView
):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CourseStatusView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]

    def patch(self, request, pk):

        try:
            course = Course.objects.get(id=pk)

        except Course.DoesNotExist:
            return Response(
                {"error": "Course not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        course.status = request.data.get(
            "status",
            course.status
        )

        course.save()

        return Response({
            "message": "Status Updated",
            "status": course.status
        })
    

from .models import Subject
from .serializers import SubjectSerializer

class SubjectCreateView(
    generics.CreateAPIView
):

    queryset = Subject.objects.all()

    serializer_class = SubjectSerializer

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]


class SubjectListView(
    generics.ListAPIView
):

    queryset = Subject.objects.all()

    serializer_class = SubjectSerializer

    permission_classes = [
        IsAuthenticated
    ]


class SubjectDetailView(
    generics.RetrieveAPIView
):

    queryset = Subject.objects.all()

    serializer_class = SubjectSerializer

    permission_classes = [
        IsAuthenticated
    ]



class SubjectUpdateView(
    generics.UpdateAPIView
):

    queryset = Subject.objects.all()

    serializer_class = SubjectSerializer

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]


class SubjectDeleteView(
    generics.DestroyAPIView
):

    queryset = Subject.objects.all()

    serializer_class = SubjectSerializer

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]



class CourseSubjectsView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, pk):

        subjects = Subject.objects.filter(
            course_id=pk
        )

        serializer = SubjectSerializer(
            subjects,
            many=True
        )

        return Response(serializer.data)