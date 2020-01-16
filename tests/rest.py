from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from scoped_rbac.rest import AccessControlledModelViewSet, DefaultPageNumberPagination
from scoped_rbac.permissions import DEFAULT_CONTEXT, IsAuthorized
from .models import ExampleRbacContext
from .serializers import ExamleRbacContextSerializer


class ExampleRbacContextViewSet(AccessControlledModelViewSet):
    queryset = ExampleRbacContext.objects.all()
    serializer_class = ExamleRbacContextSerializer
    pagination_class = DefaultPageNumberPagination
    permission_classes = [IsAuthorized]

    def context_id_for(self, request):
        return DEFAULT_CONTEXT

    @property
    def detail_iri(self):
        return ExampleRbacContext.resource_type.iri
