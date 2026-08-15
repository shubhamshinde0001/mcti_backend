from django.db import models
from courses.models import Course
from accounts.models import Teacher


class Batch(models.Model):

    STATUS_CHOICES = (
        ('UPCOMING', 'Upcoming'),
        ('ONGOING', 'Ongoing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )

    batch_name = models.CharField(
        max_length=200,
        unique=True
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='batches'
    )

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    start_date = models.DateField()

    end_date = models.DateField()

    batch_timing = models.CharField(
        max_length=100
    )

    capacity = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='UPCOMING'
    )

    room_number = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.batch_name