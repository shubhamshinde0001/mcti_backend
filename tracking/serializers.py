from rest_framework import serializers
from .models import StudentTracking


class StudentTrackingSerializer(
    serializers.ModelSerializer
):

    student_name = serializers.CharField(
        source='student.first_name',
        read_only=True
    )

    class Meta:

        model = StudentTracking

        fields = '__all__'


