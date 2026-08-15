from django.db import models

class Course(models.Model):
    COURSE_STATUS = (
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    )

    course_name = models.CharField( max_length=200, unique=True)
    description = models.TextField()
    duration_months = models.IntegerField()
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=COURSE_STATUS, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.course_name


from django.db import models


class Subject(models.Model):

    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="subjects"
    )

    subject_name = models.CharField(
        max_length=200
    )

    module = models.CharField(
        max_length=200,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    duration_days = models.PositiveIntegerField(
        default=1
    )

    order = models.PositiveIntegerField(
        default=1
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["order"]

    def __str__(self):

        return self.subject_name


class Topic(models.Model):

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="topics"
    )

    topic_name = models.CharField(max_length=200)

    order = models.PositiveIntegerField(default=1)

    duration_hours = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.topic_name