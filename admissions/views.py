from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated
)

from .serializers import (
    AdmissionSerializer
)

from accounts.permissions import (
    IsHeadAdmin
)



class AdmissionCreateView(
    APIView
):

    permission_classes = [
        IsAuthenticated,
        IsHeadAdmin
    ]

    def post(
        self,
        request
    ):

        serializer = AdmissionSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        data = serializer.save()

        return Response({
            "message":
            "Admission Successful",

            "data": data
        })
    

