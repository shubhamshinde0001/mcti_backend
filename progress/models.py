from django.db import models

from accounts.models import Student
from courses.models import Subject,Topic


class StudentSubjectProgress(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    is_completed = models.BooleanField(
        default=False
    )

    completed_date = models.DateField(
        null=True,
        blank=True
    )

    class Meta:
        unique_together = (
            "student",
            "subject"
        )

    def __str__(self):
        return f"{self.student} - {self.subject}"


class StudentTopicProgress(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE
    )

    is_completed = models.BooleanField(
        default=False
    )

    completed_date = models.DateField(
        null=True,
        blank=True
    )

    class Meta:
        unique_together = (
            "student",
            "topic"
        )