from decimal import Decimal

from django.db.models import Sum
from django.utils import timezone

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import *
from .serializers import *
from .permissions import IsHeadAdmin

class CreateFeeStructureView(
    generics.CreateAPIView
):

    queryset = FeeStructure.objects.all()

    serializer_class = FeeStructureSerializer

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]


class FeeStructureListView(
    generics.ListAPIView
):

    queryset = FeeStructure.objects.all()

    serializer_class = FeeStructureSerializer

    permission_classes = [
        IsAuthenticated
    ]


class StudentFeeListView(
    generics.ListAPIView
):

    queryset = StudentFee.objects.select_related(
        "enrollment__student__user",
        "enrollment__batch__course"
    )

    serializer_class = StudentFeeSerializer

    permission_classes = [
        IsAuthenticated
    ]


class StudentFeeDetailView(
    generics.RetrieveAPIView
):

    queryset = StudentFee.objects.select_related(
        "enrollment__student__user",
        "enrollment__batch__course"
    )

    serializer_class = StudentFeeSerializer

    permission_classes = [
        IsAuthenticated
    ]


class PendingFeesView(
    generics.ListAPIView
):

    serializer_class = StudentFeeSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return StudentFee.objects.exclude(
            status="PAID"
        ).select_related(
            "enrollment__student__user",
            "enrollment__batch__course"
        )


class FeeDashboardView(
    generics.GenericAPIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        total_fee = StudentFee.objects.aggregate(
            total=Sum("final_fee")
        )["total"] or Decimal("0")

        paid = StudentFee.objects.aggregate(
            total=Sum("paid_amount")
        )["total"] or Decimal("0")

        balance = StudentFee.objects.aggregate(
            total=Sum("balance_amount")
        )["total"] or Decimal("0")

        pending = StudentFee.objects.exclude(
            status="PAID"
        ).count()

        return Response({

            "students":
                StudentFee.objects.count(),

            "total_fee":
                total_fee,

            "paid":
                paid,

            "pending_amount":
                balance,

            "pending_students":
                pending

        })


class RecordPaymentView(
    generics.CreateAPIView
):

    queryset = Payment.objects.all()

    serializer_class = PaymentSerializer

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]

    def perform_create(
        self,
        serializer
    ):

        receipt = (
            "RCP"
            + timezone.now().strftime("%Y")
            + str(
                Payment.objects.count() + 1
            ).zfill(5)
        )

        serializer.save(

            received_by=self.request.user,

            receipt_number=receipt

        )

class PaymentHistoryView(
    generics.ListAPIView
):

    serializer_class = PaymentSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Payment.objects.filter(

            student_fee_id=self.kwargs[
                "student_fee_id"
            ]

        ).select_related(

            "received_by",
            "student_fee__enrollment__student__user"

        ).order_by(
            "-payment_date"
        )









# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated

# from .models import *
# from .serializers import *
# from .permissions import IsHeadAdmin


# class CreateFeeStructureView(
#     generics.CreateAPIView
# ):

#     queryset = FeeStructure.objects.all()

#     serializer_class = (
#         FeeStructureSerializer
#     )

#     permission_classes = [
#         IsAuthenticated,
#         IsHeadAdmin
#     ]


# class FeeStructureListView(
#     generics.ListAPIView
# ):

#     queryset = FeeStructure.objects.all()

#     serializer_class = (
#         FeeStructureSerializer
#     )

#     permission_classes = [
#         IsAuthenticated
#     ]


# class CreateStudentFeeView(
#     generics.CreateAPIView
# ):

#     queryset = StudentFee.objects.all()

#     serializer_class = (
#         StudentFeeSerializer
#     )

#     permission_classes = [
#         IsAuthenticated,
#         IsHeadAdmin
#     ]

# class RecordPaymentView(
#     generics.CreateAPIView
# ):

#     queryset = Payment.objects.all()

#     serializer_class = (
#         PaymentSerializer
#     )

#     permission_classes = [
#         IsAuthenticated,
#         IsHeadAdmin
#     ]


# class StudentFeeDetailView(
#     generics.RetrieveAPIView
# ):

#     queryset = StudentFee.objects.all()

#     serializer_class = (
#         StudentFeeSerializer
#     )

#     permission_classes = [
#         IsAuthenticated
#     ]


# class PaymentHistoryView(
#     generics.ListAPIView
# ):

#     serializer_class = (
#         PaymentSerializer
#     )

#     permission_classes = [
#         IsAuthenticated
#     ]

#     def get_queryset(self):

#         student_fee_id = self.kwargs[
#             'student_fee_id'
#         ]

#         return Payment.objects.filter(
#             student_fee_id=student_fee_id
#         )
    

# class PendingFeesView(
#     generics.ListAPIView
# ):

#     serializer_class = (
#         StudentFeeSerializer
#     )

#     permission_classes = [
#         IsAuthenticated,
#         IsHeadAdmin
#     ]

#     def get_queryset(self):

#         return StudentFee.objects.exclude(
#             status='PAID'
#         )