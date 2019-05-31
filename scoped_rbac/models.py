from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from .registry import ResourceType
from .policy_json import json_loads_policy
from .registry import register_access_controlled_model


class IdentifiedByIRI(models.Model):
    iri = models.CharField(primary_key=True, max_length=1024)
    display_name = models.CharField(max_length=256)
    description = models.TextField(null=True)

    class Meta:
        abstract = True


class Context(models.Model):
    """
    Instances of this class reflect other model instances that are RBAC access control
    contexts for other resources. When those model instances are deleted the context is
    left in place to preserve the access control on existing resources that may have
    been orphaned by the deletion of the original object.
    """

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        unique_together = ("content_type", "object_id")


def create_context_on_save(sender, instance, created, *args, **kwargs):
    if created:
        instance._rbac_context.create(**{"content_object": instance})


class RbacContext(models.Model):
    """
    Model classes that constitute access control contexts should subclass this class.
    Classes that subclass this class will automatically create an associated Context
    instance when created and save.
    """

    _rbac_context = GenericRelation(Context)

    @property
    def rbac_context(self):
        return self._rbac_context.get()

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        models.signals.post_save.connect(create_context_on_save, sender=cls, weak=False)

    class Meta:
        abstract = True


class AccessControlled(models.Model):
    """
    Model classes that will be access controlled in a `rest_framework` view should
    subclass this class.

    Subclasses **MUST** define a `resource_type: ResourceType` property.
    """

    rbac_context = models.ForeignKey(Context, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        register_access_controlled_model(cls)


class Role(IdentifiedByIRI, AccessControlled, models.Model):
    definition_json = models.TextField(null=False)

    # Required by AccessControlled
    resource_type = ResourceType(
        "rbac.Role", "Role", "A Role definition as a JSON resource."
    )

    @property
    def as_policy(self):
        return json_loads_policy(self.definition_json)


class RoleAssignment(AccessControlled, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    resource_type = ResourceType(
        "rbac.RoleAssignment",
        "RoleAssignment",
        "The assignment of an rbac.Role to a User.",
    )
