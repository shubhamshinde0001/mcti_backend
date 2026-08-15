from rest_framework import serializers
from accounts.models import Teacher

class TeacherSerializer(
    serializers.ModelSerializer
):

    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    email = serializers.CharField(
        source='user.email',
        read_only=True
    )

    class Meta:

        model = Teacher

        fields = '__all__'

from accounts.models import User

class CreateTeacherSerializer(serializers.ModelSerializer):

    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Teacher
        exclude = ["user"]

    def create(self, validated_data):

        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role="TEACHER"
        )

        return Teacher.objects.create(
            user=user,
            **validated_data
        )

    def to_representation(self, instance):
        return TeacherSerializer(instance).data

# class CreateTeacherSerializer(
#     serializers.ModelSerializer
# ):

#     username = serializers.CharField()
#     email = serializers.EmailField()
#     password = serializers.CharField(
#         write_only=True
#     )

#     class Meta:

#         model = Teacher

#         exclude = ['user']

#     def create(self, validated_data):

#         username = validated_data.pop(
#             'username'
#         )

#         email = validated_data.pop(
#             'email'
#         )

#         password = validated_data.pop(
#             'password'
#         )

#         user = User.objects.create_user(

#             username=username,
#             email=email,
#             password=password,
#             role='TEACHER'
#         )

#         teacher = Teacher.objects.create(
#             user=user,
#             **validated_data
#         )

#         return teacher
    
