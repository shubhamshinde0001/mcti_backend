from django.db import models
from accounts.models import User
from courses.models import Course


class FeeStructure(models.Model):

    course = models.OneToOneField(
        Course,
        on_delete=models.CASCADE,
        related_name='fee_structure'
    )

    total_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    registration_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    installment_allowed = models.BooleanField(
        default=True
    )

    number_of_installments = models.PositiveIntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.course.course_name

from enrollments.models import Enrollment


class StudentFee(models.Model):

    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="student_fee"
    )

    course_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    final_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    balance_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("PENDING","Pending"),
            ("PARTIAL","Partial"),
            ("PAID","Paid")
        ],
        default="PENDING"
    )

    remarks = models.TextField(
        blank=True
    )

    created_at=models.DateTimeField(auto_now_add=True)


from django.db import models
from accounts.models import User


class Payment(models.Model):

    PAYMENT_MODES = (
        ("CASH", "Cash"),
        ("UPI", "UPI"),
        ("CARD", "Card"),
        ("BANK", "Bank Transfer"),
    )

    student_fee = models.ForeignKey(
        "StudentFee",
        related_name="payments",
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODES
    )

    transaction_id = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    receipt_number = models.CharField(
        max_length=100,
        unique=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    received_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="received_payments"
    )

    class Meta:
        ordering = ["-payment_date"]

    def __str__(self):
        return f"{self.receipt_number} - ₹{self.amount}"




from decimal import Decimal
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Payment)
def update_student_fee(sender, instance, created, **kwargs):

    if not created:
        return

    fee = instance.student_fee

    total_paid = fee.payments.aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0")

    fee.paid_amount = total_paid

    fee.balance_amount = (
        fee.final_fee - total_paid
    )

    if fee.balance_amount <= 0:
        fee.balance_amount = Decimal("0")
        fee.status = "PAID"

    elif total_paid > 0:
        fee.status = "PARTIAL"

    else:
        fee.status = "PENDING"

    fee.save()

# class StudentFee(models.Model):

#     STATUS_CHOICES = (
#         ('PAID', 'Paid'),
#         ('PARTIAL', 'Partial'),
#         ('PENDING', 'Pending'),
#     )

#     enrollment = models.OneToOneField(
#         Enrollment,
#         on_delete=models.CASCADE
#     )

#     total_fee = models.DecimalField(
#         max_digits=10,
#         decimal_places=2
#     )

#     paid_amount = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         default=0
#     )

#     balance_amount = models.DecimalField(
#         max_digits=10,
#         decimal_places=2
#     )

#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default='PENDING'
#     )

#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )

#     def __str__(self):
#         return self.enrollment.student.user.username


# class Payment(models.Model):

#     PAYMENT_MODES = (
#         ('CASH', 'Cash'),
#         ('UPI', 'UPI'),
#         ('CARD', 'Card'),
#         ('BANK', 'Bank Transfer'),
#     )

#     student_fee = models.ForeignKey(
#         StudentFee,
#         on_delete=models.CASCADE,
#         related_name='payments'
#     )

#     amount = models.DecimalField(
#         max_digits=10,
#         decimal_places=2
#     )

#     payment_mode = models.CharField(
#         max_length=20,
#         choices=PAYMENT_MODES
#     )

#     transaction_id = models.CharField(
#         max_length=200,
#         blank=True,
#         null=True
#     )

#     payment_date = models.DateTimeField(
#         auto_now_add=True
#     )

#     remarks = models.TextField(
#         blank=True,
#         null=True
#     )

#     receipt_number = models.CharField(
#         max_length=50,
#         unique=True
#     )

#     received_by = models.ForeignKey(
#         'accounts.User',
#         on_delete=models.SET_NULL,
#         null=True
#     )

#     def __str__(self):
#         return self.receipt_number


# from django.db.models.signals import post_save
# from django.dispatch import receiver


# @receiver(post_save, sender=Payment)
# def update_student_fee(sender, instance, created, **kwargs):

#     if created:

#         fee = instance.student_fee

#         total_paid = fee.payments.all().aggregate(
#             total=models.Sum('amount')
#         )['total'] or 0

#         fee.paid_amount = total_paid

#         fee.balance_amount = (
#             fee.total_fee - total_paid
#         )

#         if fee.balance_amount <= 0:
#             fee.status = 'PAID'

#         elif total_paid > 0:
#             fee.status = 'PARTIAL'

#         else:
#             fee.status = 'PENDING'

#         fee.save()
    

