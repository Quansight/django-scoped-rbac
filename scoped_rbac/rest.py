from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Context, Role, RoleAssignment
from .permissions import DEFAULT_CONTEXT
from .serializers import (
    ContextSerializer,
    RoleSerializer,
    RoleAssignmentSerializer,
    UserSerializer,
)


class DefaultPageNumberPagination(PageNumberPagination):
    page_size = 100


class AccessControlledAPIView:
    """
    This `APIView` interface is required for non-object based views in combination with
    the `IsAuthorized` permission class.
    """

    def context_id_for(self, request):
        """
        Subclasses **MUST** override this method.
        """

        raise NotImplementedError()

    def resource_type_iri_for(self, request):
        if request.resolver_match.url_name.endswith("-list"):
            return self.collection_iri
        return self.detail_iri

    @property
    def detail_iri(self):
        """
        Subclasses **MUST** override this method.
        """
        raise NotImplementedError()

    @property
    def collection_iri(self):
        return f"collection<{self.detail_iri}>"


class AccessControlledModelViewSet(ModelViewSet, AccessControlledAPIView):
    def get_success_headers(self, data):
        try:
            return {
                "Location": reverse(self.basename + "-detail", args=[str(data["id"])])
            }
        except (TypeError, KeyError):
            return {}


class ContextViewSet(AccessControlledModelViewSet):
    """
    TODO restrict queryset to authorized contexts for user
    """

    queryset = Context.objects.all()
    serializer_class = ContextSerializer
    pagination_class = DefaultPageNumberPagination

    def context_id_for(self, request):
        return DEFAULT_CONTEXT

    @property
    def detail_iri(self):
        return Context.resource_type.iri


class RoleViewSet(AccessControlledModelViewSet):
    """
    TODO restrict queryset to authorized contexts for user
    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    pagination_class = DefaultPageNumberPagination

    def context_id_for(self, request):
        return DEFAULT_CONTEXT

    @property
    def detail_iri(self):
        return Role.resource_type.iri


class RoleAssignmentViewSet(AccessControlledModelViewSet):
    """
    TODO restrict queryset to authorized contexts for user
    """

    queryset = RoleAssignment.objects.all()
    serializer_class = RoleAssignmentSerializer
    pagination_class = DefaultPageNumberPagination

    def context_id_for(self, request):
        return DEFAULT_CONTEXT

    @property
    def detail_iri(self):
        return RoleAssignment.resource_type.iri


class UserViewSet(AccessControlledModelViewSet):
    """
    API which allows users to be viewed or edited.
    TODO restrict queryset to authorized contexts for user
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = DefaultPageNumberPagination
