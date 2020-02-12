from django.db import models
from scoped_rbac.models import AccessControlledModel, IdentifiedByIRI, RbacContext
from scoped_rbac.registry import ResourceType

class ScopedRbacTestModel(models.Model):
    """Mixin class for models used in testing."""

    class Meta:
        app_label = "tests"
        abstract = True


class ExampleRbacContext(ScopedRbacTestModel, AccessControlledModel, RbacContext):

    class Meta:
        get_latest_by = 'updated_at'

    name = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    resource_type = ResourceType(
        "rbac.ExampleRbacContext",
        "ExampleRbacContext",
        "An example context for testing and demonstration purposes.",
    )


