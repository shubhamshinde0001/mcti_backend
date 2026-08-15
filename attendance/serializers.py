from rest_framework import serializers
from .models import Attendance


class AttendanceSerializer(
    serializers.ModelSerializer
):

    student_name = serializers.CharField(
        source='enrollment.student.user.username',
        read_only=True
    )

    batch_name = serializers.CharField(
        source='enrollment.batch.batch_name',
        read_only=True
    )

    class Meta:
        model = Attendance
        fields = '__all__'