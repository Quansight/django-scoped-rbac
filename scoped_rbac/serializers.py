from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Context, Role, RoleAssignment, ContentType


# Needs to be able to create a hyperlink to the related contenttype
class ContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Context
        fields = "__all__"


class ContentTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContentType
        fields = "__all__"


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class RoleAssignmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RoleAssignment
        fields = "__all__"


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """User Serialization"""

    class Meta:
        model = User
        fields = ("url", "username", "email", "first_name", "last_name", "id")
