from rest_framework.pagination import PageNumberPagination
from scoped_rbac.rest import AccessControlledModelViewSet, DefaultPageNumberPagination
from .models import ExampleRbacContext
from .serializers import ExamleRbacContextSerializer


class ExampleRbacContextViewSet(AccessControlledModelViewSet):
    queryset = ExampleRbacContext.objects.all()
    serializer_class = ExamleRbacContextSerializer
    pagination_class = DefaultPageNumberPagination
