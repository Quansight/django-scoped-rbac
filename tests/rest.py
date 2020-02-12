from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_condition import last_modified, condition
from rest_framework_extensions.etag.decorators import etag
from rest_framework_extensions.etag.mixins import ETAGMixin
from scoped_rbac.rest import AccessControlledModelViewSet, DefaultPageNumberPagination
from scoped_rbac.permissions import DEFAULT_CONTEXT, IsAuthorized
from .models import ExampleRbacContext
from .serializers import ExampleRbacContextSerializer


def calculate_collection_last_modified(request, *args, **kwargs):
    from datetime import datetime
    return datetime.now()


def calculate_last_modified(request, *args, **kwargs): #, pk):
    return ExampleRbacContext.last_modified_for(pk)


def calculate_etag(request, *args, **kwargs):
    return '"foo"'


class ExampleRbacContextViewSet(AccessControlledModelViewSet):

    queryset = ExampleRbacContext.objects.all()
    serializer_class = ExampleRbacContextSerializer
    pagination_class = DefaultPageNumberPagination
    permission_classes = [IsAuthorized]

    def context_id_for(self, request):
        return DEFAULT_CONTEXT
        # TODO Is this a collection or an item?
        # if request.method = "POST":
        # return DEFAULT_CONTEXT
        # else:
        # return item

    def resource_type_iri_for(self, request):
        # TODO is this the collection or an item?
        # Also... need an IRI for collections...
        return f"{ExampleRbacContext.resource_type.iri}"

    @condition(
        last_modified_func=ExampleRbacContextSerializer.collection_last_modified,
        etag_func=ExampleRbacContextSerializer.collection_etag)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        headers["etag"] = serializer.etag()
        headers["last_modified"] = serializer.last_modified()
        return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @condition(
        last_modified_func=ExampleRbacContextSerializer.last_modified_for,
        etag_func=ExampleRbacContextSerializer.etag_for)
    def retrieve(self, request, *args, **kwargs):
        ret = super().retrieve(request, *args, **kwargs)
        return ret

    @condition(
        last_modified_func=ExampleRbacContextSerializer.last_modified_for,
        etag_func=ExampleRbacContextSerializer.etag_for)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @condition(
        last_modified_func=ExampleRbacContextSerializer.last_modified_for,
        etag_func=ExampleRbacContextSerializer.etag_for)
    def destroy(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
