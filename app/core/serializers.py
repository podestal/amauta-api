from djoser.serializers import UserSerializer as BasedUserSerializer, UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth.models import Group

class UserSerializer(BasedUserSerializer):

    groups = serializers.SlugRelatedField(
        many=True,
         queryset=Group.objects.all(),
        slug_field='name',
    )

    class Meta(BasedUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'groups']

class CreateUserSerializer(UserCreateSerializer):
    
    class Meta(UserCreateSerializer.Meta):
        fields = ['id', 'username', 'email', 'password']