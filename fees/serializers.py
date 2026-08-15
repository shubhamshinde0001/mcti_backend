from rest_framework import serializers
from .models import (
    FeeStructure,
    StudentFee,
    Payment
)


class FeeStructureSerializer(serializers.ModelSerializer):

    course_name = serializers.CharField(
        source="course.course_name",
        read_only=True
    )

    class Meta:
        model = FeeStructure
        fields = "__all__"


class StudentFeeSerializer(serializers.ModelSerializer):

    student_name = serializers.CharField(
        source="enrollment.student.user.get_full_name",
        read_only=True
    )

    username = serializers.CharField(
        source="enrollment.student.user.username",
        read_only=True
    )

    student_id = serializers.CharField(
        source="enrollment.student.student_id",
        read_only=True
    )

    course = serializers.CharField(
        source="enrollment.batch.course.course_name",
        read_only=True
    )

    batch = serializers.CharField(
        source="enrollment.batch.batch_name",
        read_only=True
    )

    class Meta:

        model = StudentFee

        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):

    student_name = serializers.CharField(
        source="student_fee.enrollment.student.user.get_full_name",
        read_only=True
    )

    student_id = serializers.CharField(
        source="student_fee.enrollment.student.student_id",
        read_only=True
    )

    course = serializers.CharField(
        source="student_fee.enrollment.batch.course.course_name",
        read_only=True
    )

    received_by_name = serializers.CharField(
        source="received_by.username",
        read_only=True
    )

    class Meta:

        model = Payment

        fields = "__all__"

        read_only_fields = (
            "receipt_number",
            "received_by",
            "payment_date",
        )



# from rest_framework import serializers
# from .models import (
#     FeeStructure,
#     StudentFee,
#     Payment
# )


# class FeeStructureSerializer(
#     serializers.ModelSerializer
# ):

#     class Meta:
#         model = FeeStructure
#         fields = '__all__'


# # class StudentFeeSerializer(
# #     serializers.ModelSerializer
# # ):

# #     student_name = serializers.CharField(
# #         source='enrollment.student.user.username',
# #         read_only=True
# #     )

# #     class Meta:
# #         model = StudentFee
# #         fields = '__all__'


# class PaymentSerializer(
#     serializers.ModelSerializer
# ):

#     class Meta:
#         model = Payment
#         fields = '__all__'




# class StudentFeeSerializer(serializers.ModelSerializer):

#     student_name = serializers.CharField(
#         source="enrollment.student.user.username",
#         read_only=True
#     )

#     student_id = serializers.CharField(
#         source="enrollment.student.student_id",
#         read_only=True
#     )

#     course = serializers.CharField(
#         source="enrollment.batch.course.course_name",
#         read_only=True
#     )

#     batch = serializers.CharField(
#         source="enrollment.batch.batch_name",
#         read_only=True
#     )

#     class Meta:
#         model = StudentFee
#         fields = "__all__"

        