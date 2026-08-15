from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from enrollments.models import Enrollment
from .serializers import EnrollmentSerializer
from fees.models import StudentFee


class EnrollmentCreateView(generics.CreateAPIView):

    queryset = Enrollment.objects.all()

    serializer_class = EnrollmentSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def perform_create(self, serializer):

        enrollment = serializer.save()

        course_fee = enrollment.batch.course.fees

        StudentFee.objects.create(

            enrollment=enrollment,

            course_fee=course_fee,

            discount=0,

            final_fee=course_fee,

            paid_amount=0,

            balance_amount=course_fee,

            status="PENDING",

            remarks=""

        )

class EnrollmentListView(generics.ListAPIView):

    queryset = Enrollment.objects.all()

    serializer_class = EnrollmentSerializer

    permission_classes = [
        IsAuthenticated
    ]

class EnrollmentDetailView(generics.RetrieveAPIView):

    queryset = Enrollment.objects.all()

    serializer_class = EnrollmentSerializer

    permission_classes = [
        IsAuthenticated
    ]
