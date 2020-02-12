from django.db.models import Manager
from django.db.models.query import QuerySet
from rest_framework import serializers


class EnvelopeCollectionSerializer(serializers.ListSerializer):
    def envelope_for(self, item):
        return {
            "href": self.child.absolute_url_for(item),
            "etag": self.child.etag_for(item),
            "last_modified": self.child.last_modified_for(item),
            "content": self.child.to_representation(item),
        }

    def to_representation(self, data):
        iterable = data.all() if isinstance(data, (Manager, QuerySet)) else data
        ret = [self.envelope_for(item) for item in iterable]
        return ret
