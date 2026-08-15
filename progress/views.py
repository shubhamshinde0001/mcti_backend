from datetime import date

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import Teacher
from courses.models import Subject
from accounts.models import Student
from progress.serializers import StudentSubjectProgressSerializer

from .models import StudentSubjectProgress


class MarkSubjectCompletedView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request
    ):

        # Check teacher exists
        Teacher.objects.get(
            user=request.user
        )

        student = Student.objects.get(
            id=request.data["student"]
        )

        subject = Subject.objects.get(
            id=request.data["subject"]
        )

        progress, created = StudentSubjectProgress.objects.get_or_create(

            student=student,

            subject=subject
        )

        progress.is_completed = True

        progress.completed_date = date.today()

        progress.save()

        return Response({

            "message":
            "Subject marked as completed.",

            "student":
            student.first_name,

            "subject":
            subject.subject_name
        })



class MarkSubjectPendingView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request
    ):

        progress = StudentSubjectProgress.objects.get(

            student_id=request.data["student"],

            subject_id=request.data["subject"]
        )

        progress.is_completed = False

        progress.completed_date = None

        progress.save()

        return Response({

            "message":
            "Subject marked as pending."
        })



class StudentProgressView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
        student_id
    ):

        progress = StudentSubjectProgress.objects.filter(

            student_id=student_id

        )

        serializer = StudentSubjectProgressSerializer(

            progress,

            many=True
        )

        return Response(
            serializer.data
        )




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from batches.models import Batch
from enrollments.models import Enrollment
from courses.models import Subject

from .models import StudentSubjectProgress


class BatchProgressView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, batch_id):

        batch = Batch.objects.get(id=batch_id)

        enrollments = Enrollment.objects.filter(
            batch=batch
        ).select_related("student")

        subjects = Subject.objects.filter(
            course=batch.course
        ).order_by("order")

        students = []

        for enrollment in enrollments:

            student = enrollment.student

            completed = StudentSubjectProgress.objects.filter(

                student=student,

                subject__course=batch.course,

                is_completed=True

            ).count()

            total = subjects.count()

            pending = total - completed

            percentage = 0

            if total > 0:

                percentage = round(
                    completed * 100 / total,
                    2
                )

            students.append({

                "student_id": student.id,

                "student_name": student.first_name,

                "completed": completed,

                "pending": pending,

                "percentage": percentage

            })

        return Response({

            "batch": batch.batch_name,

            "course": batch.course.course_name,

            "teacher": batch.teacher.user.username,

            "students": students

        })