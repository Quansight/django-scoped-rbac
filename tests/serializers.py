from rest_framework import serializers
from .models import ExampleRbacContext

class ExamleRbacContextSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExampleRbacContext
        fields = ("id", "name")
