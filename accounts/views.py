from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import User
from .serializers import ProfileSerializer, RegisterSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer



class RegisterView(
    generics.CreateAPIView
):

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    authentication_classes = []

from rest_framework.permissions import IsAuthenticated
from .permissions import IsHeadAdmin


class UserListView(
    generics.ListAPIView
):

    queryset = User.objects.all()

    serializer_class = UserSerializer

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class MyProfileView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        serializer = ProfileSerializer(
            request.user
        )

        return Response(
            serializer.data
        )


class LoginView(APIView):

    permission_classes = [AllowAny]

    authentication_classes = []

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response({

            "refresh": str(refresh),

            "access": str(refresh.access_token),

            "user": {

                "id": user.id,

                "username": user.username,

                "email": user.email,

                "role": user.role,

                "phone": user.phone
            }

        })


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            refresh_token = request.data["refresh"]

            token = RefreshToken(refresh_token)

            token.blacklist()

            return Response({
                "message": "Logged out successfully."
            })

        except Exception:

            return Response(
                {
                    "error": "Invalid refresh token."
                },
                status=400
            )