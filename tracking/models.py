from django.db import models

# Create your models here.
from django.db import models
from accounts.models import Student


class StudentTracking(models.Model):

    STATUS_CHOICES = (
        ('IN', 'Checked In'),
        ('OUT', 'Checked Out'),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='tracking_logs'
    )

    date = models.DateField()

    check_in = models.DateTimeField(
        null=True,
        blank=True
    )

    check_out = models.DateTimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='IN'
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return (
            f"{self.student.student_id}"
            f" - {self.date}"
        )