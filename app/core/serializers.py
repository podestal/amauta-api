from djoser.serializers import UserSerializer as BasedUserSerializer, UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

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



    # groups = serializers.ListField(
    #     child=serializers.CharField(), 
    #     required=False  
    # )
    
    # class Meta(UserCreateSerializer.Meta):
    #     fields = ['id', 'username', 'email', 'password', 'groups']

    # def validate_groups(self, value):
    #     """Ensure that group names exist in the database."""
    #     groups = Group.objects.filter(name__in=value)
    #     if len(groups) != len(value):
    #         missing_groups = set(value) - set(groups.values_list('name', flat=True))
    #         raise serializers.ValidationError(f"Invalid group names: {missing_groups}")
    #     return groups  # Return the actual Group queryset

    # def create(self, validated_data):
    #     print('validated_data', validated_data)

    #     # Pop groups before user creation to prevent direct assignment error
    #     groups = validated_data.pop('groups', [])

    #     # Create the user
    #     user = super().create(validated_data)

    #     # Assign groups after user creation
    #     user.groups.set(groups)

    #     return user