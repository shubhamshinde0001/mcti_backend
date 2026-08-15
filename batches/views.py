from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Batch
from .serializers import BatchSerializer
from .permissions import IsHeadAdmin


class BatchCreateView(
    generics.CreateAPIView
):

    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]


class BatchListView(
    generics.ListAPIView
):

    queryset = Batch.objects.all()

    serializer_class = BatchSerializer

    permission_classes = [
        IsAuthenticated
    ]


class BatchDetailView(
    generics.RetrieveAPIView
):

    queryset = Batch.objects.all()

    serializer_class = BatchSerializer

    permission_classes = [
        IsAuthenticated
    ]

class BatchUpdateView(
    generics.UpdateAPIView
):

    queryset = Batch.objects.all()

    serializer_class = BatchSerializer

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]


class BatchDeleteView(
    generics.DestroyAPIView
):

    queryset = Batch.objects.all()

    serializer_class = BatchSerializer

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.models import Teacher


class AssignTeacherView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]

    def patch(self, request, pk):

        try:
            batch = Batch.objects.get(id=pk)

            teacher = Teacher.objects.get(
                id=request.data['teacher_id']
            )

        except Exception:
            return Response(
                {"error": "Invalid data"},
                status=status.HTTP_400_BAD_REQUEST
            )

        batch.teacher = teacher

        batch.save()

        return Response({
            "message":
            "Teacher assigned successfully"
        })
    

class BatchStatusView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]

    def patch(self, request, pk):

        try:

            batch = Batch.objects.get(id=pk)

        except Batch.DoesNotExist:

            return Response(
                {"error": "Batch not found"},
                status=404
            )

        batch.status = request.data.get(
            "status",
            batch.status
        )

        batch.save()

        return Response({
            "message": "Status Updated",
            "status": batch.status
        })
    

