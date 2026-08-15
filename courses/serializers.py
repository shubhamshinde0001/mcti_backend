
from rest_framework import serializers


from .models import Subject


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:

        model = Subject

        fields = "__all__"

from .models import Course

class CourseSerializer(serializers.ModelSerializer):

    subjects = SubjectSerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = Course

        fields = "__all__"