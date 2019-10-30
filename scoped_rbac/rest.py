from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Context, Role, RoleAssignment
from .serializers import (
    ContextSerializer,
    RoleSerializer,
    RoleAssignmentSerializer,
    UserSerializer,
)


class AccessControlledAPIView(APIView):
    """
    This `APIView` interface is required for non-object based views in combination with
    the `IsAuthorized` permission class.
    """

    def context_id_for(request):
        """
        Subclasses **MUST** override this method.
        """

        raise "Not implemented"

    def resource_type_iri_for(request):
        """
        Subclasses **MUST** override this method.
        """

        raise "Not implemented"


class AccessControlledModelViewSet(AccessControlledAPIView, ModelViewSet):
    pass


class ContextViewSet(AccessControlledModelViewSet):
    """
    TODO restrict queryset to authorized contexts for user
    """

    queryset = Context.objects.all()
    serializer_class = ContextSerializer


class RoleViewSet(AccessControlledModelViewSet):
    """
    TODO restrict queryset to authorized contexts for user
    """

    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleAssignmentViewSet(AccessControlledModelViewSet):
    """
    TODO restrict queryset to authorized contexts for user
    """

    queryset = RoleAssignment.objects.all()
    serializer_class = RoleAssignmentSerializer


class UserViewSet(AccessControlledModelViewSet):
    """
    API which allows users to be viewed or edited.
    TODO restrict queryset to authorized contexts for user
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
