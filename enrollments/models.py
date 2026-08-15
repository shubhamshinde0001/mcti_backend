from django.db import models
from accounts.models import Student
from batches.models import Batch


class Enrollment(models.Model):

    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('DROPPED', 'Dropped'),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE
    )

    enrolled_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    class Meta:
        unique_together = ('student', 'batch')

    def __str__(self):
        return f"{self.student} - {self.batch}"