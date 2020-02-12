from django.db.models import Manager
from django.db.models.query import QuerySet
from rest_framework import serializers


class EnvelopeItemSerializer:
    """Items that will be serialized in an envelope **MUST** be serialized by a class
    that satisfies this interface.
    """
    def absolute_url_for(self, item):
        """Given an instance of the item to be serialized return its absolute url for
        inclusion in the envelope's properties.
        """
        raise NotImplementedError()

    def etag_for(self, item=None, *args, pk=None, **kwargs):
        """Given the primary key ``pk`` or the instance ``item`` to be serialized return
        an etag for the indiciated resource.
        """
        raise NotImplementedError()

    def last_modified_for(self, item=None, *args, pk=None, **kwargs):
        """Given the primary key ``pk`` or the instance ``item`` to be serialized return
        the datetime of the last modification made to the indicated resource.
        """
        raise NotImplementedError()


class EnvelopeCollectionSerializer(serializers.ListSerializer):
    """Serliaize items in a list wrapped in an evenlope containing caching headers and
    other properties.
    """
    def envelope_for(self, item):
        """Return an envelope containing caching headers and other properties for the
        ``item`` being serialized, as well as the serialized representation of the
        ``item``.
        """
        return {
            "href": self.child.absolute_url_for(item),
            "etag": self.child.etag_for(item),
            "last_modified": self.child.last_modified_for(item),
            "content": self.child.to_representation(item),
        }

    def to_representation(self, data):
        """Return the serialized representation of the list with every item in the list
        wrapped in an envelope containing the caching headers and other properties
        associated with each item in the list.
        """
        iterable = data.all() if isinstance(data, (Manager, QuerySet)) else data
        ret = [self.envelope_for(item) for item in iterable]
        return ret
