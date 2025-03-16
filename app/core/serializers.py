from djoser.serializers import UserSerializer as BasedUserSerializer, UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

user = get_user_model()

class UserSerializer(BasedUserSerializer):

    groups = serializers.SlugRelatedField(
        many=True,
         queryset=Group.objects.all(),
        slug_field='name',
    )

    class Meta(BasedUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'groups', 'profile']

class CreateUserSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        fields = ['id', 'username', 'email', 'password', 'profile', 'first_name', 'last_name']

    def create(self, validated_data):
        user = super().create(validated_data)
        self.send_welcome_email(user)
        return user
    
    def send_welcome_email(self, user):
        """Send a welcome email with password reset link and username"""
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        subject = "🎉 ¡Bienvenido a Amautapp! Configura tu contraseña"
        
        # Render HTML email template
        message = render_to_string("emails/welcome_email.html", {
            "user": user,
            "frontend_url": settings.FRONTEND_URL,
            "uid": uid,
            "token": token,
            "username": user.username  # Ensure the template receives this
        })

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

    # def send_welcome_email(self, user):
    #     """Send a welcome email with password reset link"""
    #     uid = urlsafe_base64_encode(force_bytes(user.pk))
    #     token = default_token_generator.make_token(user)

    #     subject = "🎉 ¡Bienvenido a Amautapp! Configura tu contraseña"
        
    #     # Render HTML email template
    #     message = render_to_string("emails/welcome_email.html", {
    #         "user": user,
    #         "frontend_url": settings.FRONTEND_URL,
    #         "uid": uid,
    #         "token": token
    #     })

    #     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

