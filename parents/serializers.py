from rest_framework import serializers
from accounts.models import Parent, User

from rest_framework import serializers
from accounts.models import Parent

class ParentSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    class Meta:
        model = Parent
        fields = "__all__"

from accounts.models import User

class CreateParentSerializer(serializers.ModelSerializer):

    username = serializers.CharField(write_only=True)

    email = serializers.EmailField(write_only=True)

    password = serializers.CharField(write_only=True)

    class Meta:
        model = Parent
        exclude = ["user"]

    def create(self, validated_data):

        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role="PARENT"
        )

        return Parent.objects.create(
            user=user,
            **validated_data
        )

    def to_representation(self, instance):
        return ParentSerializer(instance).data