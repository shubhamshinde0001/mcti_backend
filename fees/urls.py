from django.urls import path

from .views import *

urlpatterns = [

    # Fee Structure

    path(
        "fee-structure/",
        FeeStructureListView.as_view()
    ),

    path(
        "fee-structure/create/",
        CreateFeeStructureView.as_view()
    ),

    # Student Fees

    path(
        "student-fees/",
        StudentFeeListView.as_view()
    ),

    path(
        "student-fees/<int:pk>/",
        StudentFeeDetailView.as_view()
    ),

    path(
        "pending-fees/",
        PendingFeesView.as_view()
    ),

    # Dashboard

    path(
        "dashboard/",
        FeeDashboardView.as_view()
    ),

    # Payments

    path(
        "payments/",
        PaymentHistoryView.as_view()
    ),

    path(
        "payments/<int:student_fee_id>/",
        PaymentHistoryView.as_view()
    ),

    path(
        "payments/create/",
        RecordPaymentView.as_view()
    ),
]