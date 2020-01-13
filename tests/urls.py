import scoped_rbac.urls
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from . import rest

# from . import rest

router = DefaultRouter()
router.register(r"example-rbac-contexts", rest.ExampleRbacContextViewSet)
router.registry.extend(scoped_rbac.urls.router.registry)
schema_view = get_schema_view("Test Scoped RBAC API")

urlpatterns = [
    url(r"^api/", include(router.urls), name="api"),
    url(r"^api/schema", schema_view, name="api-schema"),
    url(
        r"^api/rest-framework/auth",
        include("rest_framework.urls", namespace="rest_framework"),
    ),
]
