from rest_framework import serializers

from .models import StudentSubjectProgress


class StudentSubjectProgressSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = StudentSubjectProgress

        fields = "__all__"