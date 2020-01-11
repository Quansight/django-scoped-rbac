from django.db import models
from scoped_rbac.models import IdentifiedByIRI, RbacContext


class ScopedRbacTestModel(models.Model):
    """Mixin class for models used in testing."""

    class Meta:
        app_label = "tests"
        abstract = True


class ExampleRbacContext(ScopedRbacTestModel, RbacContext):
    name = models.CharField(max_length=128)
