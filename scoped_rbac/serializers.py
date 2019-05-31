from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Context, Role, RoleAssignment


class ContextSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Context


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role


class RoleAssignmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RoleAssignment


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """User Serialization"""

    class Meta:
        model = User
        fields = ("url", "username", "email", "first_name", "last_name", "id")
