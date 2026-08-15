from rest_framework import serializers
from .models import Batch


class BatchSerializer(serializers.ModelSerializer):

    course_name = serializers.CharField(
        source='course.course_name',
        read_only=True
    )

    teacher_name = serializers.CharField(
        source='teacher.user.username',
        read_only=True
    )

    class Meta:
        model = Batch
        fields = '__all__'