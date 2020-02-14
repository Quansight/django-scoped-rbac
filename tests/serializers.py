from datetime import datetime
from drf_envelopes.serializers import (
        EnvelopeCollectionSerializer,
        EnvelopeItemSerializer,
        )
from rest_framework import serializers
from rest_framework.reverse import reverse_lazy
from .models import ExampleRbacContext
import hashlib


class ExampleRbacContextSerializer(
        EnvelopeItemSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ExampleRbacContext
        fields = ("id", "name")
        list_serializer_class = EnvelopeCollectionSerializer

    def absolute_url_for(self, item):
        return reverse_lazy("examplerbaccontext-detail", pk=item.pk)

    @classmethod
    def etag_for(cls, item=None, *arg, pk=None, **kwarg):
        if pk is not None:
            item = ExampleRbacContext.objects.get(pk=pk)
        return hashlib.md5(f"{item.name} {item.updated_at}".encode("utf-8")).hexdigest()

    @classmethod
    def last_modified_for(cls, item=None, *arg, pk=None, **kwarg):
        if pk is not None:
            item = ExampleRbacContext.objects.get(pk=pk)
        return item.updated_at

    @classmethod
    def collection_last_modified(cls, request, *args, **kwargs):
        try:
            return ExampleRbacContext.objects.latest().updated_at
        except ExampleRbacContext.DoesNotExist:
            return datetime.now()

    @classmethod
    def collection_etag(cls, request, *args, **kwargs):
        try:
            return hashlib.md5(
                f"examplerbaccontext-list {ExampleRbacContext.objects.latest().updated_at}".encode(
                    "utf-8"
                )
            ).hexdigest()
        except ExampleRbacContext.DoesNotExist:
            return hashlib.md5(
                f"examplerbaccontext-list {datetime.now()}".encode("utf-8")
            ).hexdigest()
