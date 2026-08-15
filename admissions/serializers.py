from datetime import timezone

from rest_framework import serializers
from django.db import transaction

from accounts.models import (
    User,
    Parent,
    Student
)

from batches.models import Batch

from enrollments.models import Enrollment

from fees.models import (
    StudentFee,
    FeeStructure
)


class AdmissionSerializer(
    serializers.Serializer
):

    # Parent Details

    parent_username = serializers.CharField()

    parent_email = serializers.EmailField()

    parent_password = serializers.CharField()

    father_name = serializers.CharField()

    mother_name = serializers.CharField(
        required=False
    )

    parent_mobile = serializers.CharField()

    occupation = serializers.CharField()

    address = serializers.CharField()

    # Student Details

    student_username = serializers.CharField()

    student_email = serializers.EmailField()

    student_password = serializers.CharField()

    first_name = serializers.CharField()

    last_name = serializers.CharField()

    gender = serializers.CharField()

    date_of_birth = serializers.DateField()

    student_mobile = serializers.CharField()

    batch_id = serializers.IntegerField()

    @transaction.atomic
    def create(
        self,
        validated_data
    ):

        parent_user = User.objects.create_user(

            username=validated_data[
                'parent_username'
            ],

            email=validated_data[
                'parent_email'
            ],

            password=validated_data[
                'parent_password'
            ],

            role='PARENT'
        )

        parent = Parent.objects.create(

            user=parent_user,

            father_name=validated_data[
                'father_name'
            ],

            mother_name=validated_data.get(
                'mother_name'
            ),

            mobile=validated_data[
                'parent_mobile'
            ],

            occupation=validated_data[
                'occupation'
            ],

            address=validated_data[
                'address'
            ]
        )

        student_user = User.objects.create_user(

            username=validated_data[
                'student_username'
            ],

            email=validated_data[
                'student_email'
            ],

            password=validated_data[
                'student_password'
            ],

            role='STUDENT'
        )


        last_student = Student.objects.count()

        student_id = (
            f"STU{last_student + 1:05d}"
        )


        student = Student.objects.create(

            user=student_user,

            parent=parent,

            student_id=student_id,

            first_name=validated_data[
                'first_name'
            ],

            last_name=validated_data[
                'last_name'
            ],

            gender=validated_data[
                'gender'
            ],

            date_of_birth=validated_data[
                'date_of_birth'
            ],

            mobile=validated_data[
                'student_mobile'
            ],

            address=validated_data[
                'address'
            ],

            admission_date=timezone.now().date()
        )


        batch = Batch.objects.get(
            id=validated_data['batch_id']
        )


        enrollment = Enrollment.objects.create(

            student=student,

            batch=batch,

            enrolled_date=timezone.now().date(),

            status='ACTIVE'
        )


        fee_structure = FeeStructure.objects.get(
            course=batch.course
        )

        StudentFee.objects.create(

            enrollment=enrollment,

            total_fee=fee_structure.total_fee,

            paid_amount=0,

            balance_amount=fee_structure.total_fee,

            status='PENDING'
        )


        return {

            "student_id":
            student.student_id,

            "student_name":
            student.first_name,

            "batch":
            batch.batch_name,

            "course":
            batch.course.course_name
        }