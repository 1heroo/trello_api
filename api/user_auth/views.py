from decouple import config
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from api.models import MyUser
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode

from .serializers import (
    RegisterSerializer,
    ResetPasswordSerializer,
    ResetPasswordCompleteSerializer,
    ChangePasswordSerializer,
)


class RegisterAPIView(APIView):

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'New user': request.data}, status=status.HTTP_201_CREATED)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def patch(self, request):
        serializer = ChangePasswordSerializer(data=request.data, instance=request.user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Message': 'Password changed'}, status=status.HTTP_200_OK)


class ActivationAPIView(APIView):

    def get(self, request, code):
        user = MyUser.objects.filter(code=code)[0]
        if not user:
            return Response({'message': 'Invalid code or user does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.code = ''
        user.save()
        return Response({'message': 'Account successfully activated'}, status=status.HTTP_201_CREATED)


class ResetPasswordAPIView(APIView):

    @swagger_auto_schema(request_body=ResetPasswordSerializer)
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'Message': 'successfully succeed'})


class PasswordTokenVerifyAPIView(APIView):

    def get(self, request, uidb64, token):
        try:
            pk = smart_str(urlsafe_base64_decode(uidb64))
            user = MyUser.objects.filter(pk=pk)[0]
            if not user:
                return Response({'Message': f'User not found with id {pk}'}, status.HTTP_400_BAD_REQUEST)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'Message': 'This token is not valid'}, status=status.HTTP_400_BAD_REQUEST)
            data = {
                'success': True,
                'message': 'Credentials Valid',
                'uidb64': uidb64,
                'token': token
            }
            return Response({'Response': data}, status=status.HTTP_202_ACCEPTED)

        except DjangoUnicodeDecodeError:
            return Response({'Message': 'Invalid uidb64'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ResetPasswordCompleteAPIView(APIView):

    @swagger_auto_schema(request_body=ResetPasswordCompleteSerializer)
    def patch(self, request):
        try:
            data = request.data
            uidb64 = data.pop('uidb64')
            token = data.pop('token')
            pk = smart_str(urlsafe_base64_decode(uidb64))

            user = MyUser.objects.filter(pk=pk)[0]

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'Message': 'This token is not valid'}, status=status.HTTP_400_BAD_REQUEST)

            if not user:
                return Response({'Message': f'User not found with id {pk}'}, status.HTTP_400_BAD_REQUEST)

            serializer = ResetPasswordCompleteSerializer(data=data, instance=user)
            serializer.is_valid()
            serializer.update(data, user)
            return Response({'Message': f'Password successfully changed!'}, status=status.HTTP_202_ACCEPTED)

        except DjangoUnicodeDecodeError:
            return Response({'Message': 'Invalid uidb64'}, status=status.HTTP_406_NOT_ACCEPTABLE)



