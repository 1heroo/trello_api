from api.models import MyUser
from rest_framework import serializers
from django.core.mail import send_mail
from django.urls import reverse

from django.core.validators import EmailValidator, RegexValidator
from decouple import config

# password reset libs
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=50)

    def validate_email(self, email):
        if MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('email already exists')
        return email

    def create(self, validated_data):
        host = config("HOST")
        password = validated_data.pop('password')
        user = MyUser(**validated_data)
        user.set_password(password)
        code = user.set_code()
        user.is_active = False
        send_mail(
            subject='Activation',
            message=f'{host}{reverse("activation-api", kwargs={"code": code})}',
            from_email='iswearican.a@gmail.com',
            recipient_list=[user.email],
            fail_silently=False
        )
        user.save()
        return user


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=(EmailValidator, )
    )

    def validate(self, attrs):
        email = attrs.get('email', None)

        user = MyUser.objects.filter(email=email)[0]
        if user:
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            # sending email
            host = config("HOST")
            body = reverse('reset-token-verify', kwargs={
                'uidb64': uidb64,
                'token': token
            })

            activation_link = '{host}{body}'.format(host=host, body=body)
            email_text = f'Dear, {user.first_name}, please click link below to reset your password \n {activation_link}'

            send_mail(
                subject='Password Reset Confirmation',
                message=email_text,
                from_email='iswearican.a@gmail.com',
                recipient_list=[email],
                fail_silently=False
            )
            return attrs
        raise serializers.ValidationError('Email Not Found!')


class ResetPasswordCompleteSerializer(serializers.Serializer):
    password = serializers.CharField(
        validators=(RegexValidator(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"), ),
        write_only=True
    )
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)

    def update(self, validated_data, instance: MyUser):
        password = validated_data.pop('password')

        if instance.check_password(password):
            raise serializers.ValidationError('New password can not be same with old one!')

        instance.set_password(password)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        validators=(RegexValidator(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"),),
        write_only=True
    )
    password_confirmation = serializers.CharField(
        validators=(RegexValidator(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"),),
        write_only=True
    )

    def update(self, instance, attr):
        password = attr.pop('password')
        password_confirmation = attr.pop('password_confirmation')

        if instance.check_password(password):
            raise serializers.ValidationError('New password can not be same with old one!')

        if password != password_confirmation:
            raise serializers.ValidationError('Passwords are not same')

        instance.set_password(password)
        instance.save()
        return instance









