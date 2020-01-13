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
        # TODO Is this a collection or an item?
        # if request.method = "POST":
        # return DEFAULT_CONTEXT
        # else:
        # return item

    def resource_type_iri_for(self, request):
        # TODO is this the collection or an item?
        # Also... need an IRI for collections...
        return f"{ExampleRbacContext.resource_type.iri}"

    def dispatch(self, *args, **kwargs):
        # import pdb; pdb.set_trace()
        return super().dispatch(*args, **kwargs)
