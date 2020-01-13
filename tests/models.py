from django.db import models
from scoped_rbac.models import AccessControlledModel, IdentifiedByIRI, RbacContext
from scoped_rbac.registry import ResourceType


class ScopedRbacTestModel(models.Model):
    """Mixin class for models used in testing."""

    class Meta:
        app_label = "tests"
        abstract = True


class ExampleRbacContext(ScopedRbacTestModel, AccessControlledModel, RbacContext):
    name = models.CharField(max_length=128)
    resource_type = ResourceType(
        "rbac.ExampleRbacContext",
        "ExampleRbacContext",
        "An example context for testing and demonstration purposes.",
    )
