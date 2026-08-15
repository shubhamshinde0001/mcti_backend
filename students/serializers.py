from rest_framework import serializers

from accounts.models import (
    Student,
    Parent,
    User
)

from progress.models import (
    StudentSubjectProgress,
    StudentTopicProgress
)

from courses.models import Topic


class StudentSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    class Meta:
        model = Student
        fields = "__all__"


class CreateStudentSerializer(serializers.ModelSerializer):

    username = serializers.CharField(write_only=True)

    email = serializers.EmailField(write_only=True)

    password = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        exclude = ["user"]

    def create(self, validated_data):

        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role="STUDENT"
        )

        return Student.objects.create(
            user=user,
            **validated_data
        )



from enrollments.models import Enrollment


class StudentEnrollmentSerializer(serializers.ModelSerializer):

    course = serializers.CharField(
        source="batch.course.course_name",
        read_only=True
    )

    batch = serializers.CharField(
        source="batch.batch_name",
        read_only=True
    )

    teacher = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = [
            "id",
            "course",
            "batch",
            "teacher",
            "status",
            "enrolled_date"
        ]

    def get_teacher(self, obj):
        return obj.batch.teacher.user.username

from rest_framework import serializers

from enrollments.models import Enrollment
from progress.models import StudentSubjectProgress


# class StudentCourseDashboardSerializer(
#     serializers.ModelSerializer
# ):

#     course = serializers.CharField(
#         source="batch.course.course_name"
#     )

#     batch = serializers.CharField(
#         source="batch.batch_name"
#     )

#     teacher = serializers.SerializerMethodField()

#     subjects = serializers.SerializerMethodField()

#     total_subjects = serializers.SerializerMethodField()

#     completed_subjects = serializers.SerializerMethodField()

#     pending_subjects = serializers.SerializerMethodField()

#     completion_percentage = serializers.SerializerMethodField()

#     class Meta:

#         model = Enrollment

#         fields = [

#             "course",

#             "batch",

#             "teacher",

#             "status",

#             "enrolled_date",

#             "subjects",

#             "total_subjects",

#             "completed_subjects",

#             "pending_subjects",

#             "completion_percentage"
#         ]

#     def get_teacher(self, obj):

#         return obj.batch.teacher.user.username

#     def get_subjects(self, obj):

#         student = obj.student

#         course = obj.batch.course

#         progress = StudentSubjectProgress.objects.filter(
#             student=student,
#             subject__course=course
#         )

#         completed_ids = progress.filter(
#             is_completed=True
#         ).values_list(
#             "subject_id",
#             flat=True
#         )

#         data = []

#         for subject in course.subjects.all().order_by("order"):

#             p = progress.filter(
#                 subject=subject
#             ).first()

#             data.append({

#                 "id": subject.id,

#                 "subject_name": subject.subject_name,

#                 "completed": subject.id in completed_ids,

#                 "completed_date":
#                 p.completed_date if p else None
#             })

#         return data

#     def get_total_subjects(self, obj):

#         return obj.batch.course.subjects.count()

#     def get_completed_subjects(self, obj):

#         return StudentSubjectProgress.objects.filter(

#             student=obj.student,

#             subject__course=obj.batch.course,

#             is_completed=True

#         ).count()

#     def get_pending_subjects(self, obj):

#         total = self.get_total_subjects(obj)

#         completed = self.get_completed_subjects(obj)

#         return total - completed

#     def get_completion_percentage(self, obj):

#         total = self.get_total_subjects(obj)

#         completed = self.get_completed_subjects(obj)

#         if total == 0:

#             return 0

#         return round(
#             completed * 100 / total,
#             2
#         )

class StudentCourseDashboardSerializer(serializers.ModelSerializer):

    course = serializers.CharField(
        source="batch.course.course_name"
    )

    batch = serializers.CharField(
        source="batch.batch_name"
    )

    teacher = serializers.SerializerMethodField()

    subjects = serializers.SerializerMethodField()

    total_subjects = serializers.SerializerMethodField()

    completed_subjects = serializers.SerializerMethodField()

    pending_subjects = serializers.SerializerMethodField()

    completion_percentage = serializers.SerializerMethodField()

    total_topics = serializers.SerializerMethodField()

    completed_topics = serializers.SerializerMethodField()

    pending_topics = serializers.SerializerMethodField()

    topic_percentage = serializers.SerializerMethodField()

    class Meta:

        model = Enrollment

        fields = [

            "course",
            "batch",
            "teacher",
            "status",
            "enrolled_date",

            "subjects",

            "total_subjects",
            "completed_subjects",
            "pending_subjects",
            "completion_percentage",

            "total_topics",
            "completed_topics",
            "pending_topics",
            "topic_percentage",
        ]

    def get_teacher(self, obj):

        if obj.batch.teacher:
            return obj.batch.teacher.user.username

        return "--"

    def get_subjects(self, obj):

        student = obj.student
        course = obj.batch.course

        subject_progress = StudentSubjectProgress.objects.filter(
            student=student,
            subject__course=course
        )

        topic_progress = StudentTopicProgress.objects.filter(
            student=student,
            topic__subject__course=course
        )

        completed_subject_ids = subject_progress.filter(
            is_completed=True
        ).values_list(
            "subject_id",
            flat=True
        )

        data = []

        for subject in course.subjects.all().order_by("order"):

            sp = subject_progress.filter(
                subject=subject
            ).first()

            topics = Topic.objects.filter(
                subject=subject
            ).order_by("order")

            topic_list = []

            completed = 0

            for topic in topics:

                tp = topic_progress.filter(
                    topic=topic
                ).first()

                is_completed = False

                completed_date = None

                if tp:

                    is_completed = tp.is_completed
                    completed_date = tp.completed_date

                if is_completed:
                    completed += 1

                topic_list.append({

                    "id": topic.id,

                    "topic_name": topic.topic_name,

                    "completed": is_completed,

                    "completed_date": completed_date

                })

            total = topics.count()

            percentage = 0

            if total > 0:
                percentage = round(completed * 100 / total, 2)

            data.append({

                "id": subject.id,

                "subject_name": subject.subject_name,

                "module": subject.module,

                "completed": subject.id in completed_subject_ids,

                "completed_date":
                sp.completed_date if sp else None,

                "total_topics": total,

                "completed_topics": completed,

                "pending_topics": total - completed,

                "percentage": percentage,

                "topics": topic_list

            })

        return data

    def get_total_subjects(self, obj):

        return obj.batch.course.subjects.count()

    def get_completed_subjects(self, obj):

        return StudentSubjectProgress.objects.filter(

            student=obj.student,

            subject__course=obj.batch.course,

            is_completed=True

        ).count()

    def get_pending_subjects(self, obj):

        return (
            self.get_total_subjects(obj)
            -
            self.get_completed_subjects(obj)
        )

    def get_completion_percentage(self, obj):

        total = self.get_total_subjects(obj)

        if total == 0:
            return 0

        return round(

            self.get_completed_subjects(obj)

            * 100 / total,

            2

        )

    def get_total_topics(self, obj):

        return Topic.objects.filter(

            subject__course=obj.batch.course

        ).count()

    def get_completed_topics(self, obj):

        return StudentTopicProgress.objects.filter(

            student=obj.student,

            topic__subject__course=obj.batch.course,

            is_completed=True

        ).count()

    def get_pending_topics(self, obj):

        return (

            self.get_total_topics(obj)

            -

            self.get_completed_topics(obj)

        )

    def get_topic_percentage(self, obj):

        total = self.get_total_topics(obj)

        if total == 0:
            return 0

        return round(

            self.get_completed_topics(obj)

            * 100 / total,

            2

        )