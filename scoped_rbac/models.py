from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from .policy_json import json_loads_policy
from .fields import JSONField
from .registry import ResourceType, register_access_controlled_model
import logging


class IdentifiedByIRI(object):
    """
    A model mixin that has an associated RDF IRI indicating its RDF type.

    Subclasses **MUST** define a `resource_type: ResourceType` property.
    """

    ...


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

    resource_type = ResourceType(
        "rbac.Context",
        "Context",
        "Generic representation of a Context in an scoped_rbac system.",
    )


def create_context_on_save(sender, instance, created, *args, **kwargs):
    if created:
        instance._rbac_context.create(**{"content_object": instance})


class RbacContext(models.Model):
    """
    Model classes that constitute access control contexts should subclass this class.
    Classes that subclass this class will automatically create and save an associated
    Context instance when created.
    """

    _rbac_context = GenericRelation(Context)

    @property
    def as_rbac_context(self):
        return self._rbac_context.get()

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        models.signals.post_save.connect(create_context_on_save, sender=cls, weak=False)

    class Meta:
        abstract = True


class AccessControlledModel(models.Model):
    """
    Model classes that will be access controlled in a `rest_framework` view should
    subclass this class.

    Subclasses **MUST** define a `resource_type: ResourceType` property.
    """


    class Meta:
        abstract = True

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        register_access_controlled_model(cls)
        cls.register_rbac_context_field()

    @classmethod
    def register_rbac_context_field(cls):
        if cls.rbac_context != AccessControlledModel.rbac_context \
                or hasattr(cls, "_rbac_context_field"):
            return
        matching_fields = filter(
            lambda x: isinstance(x, models.ForeignKey) \
                and issubclass(x.to, RbacContext),
            cls._meta.get_fields())
        if len(matching_fields) == 1:
            setattr(cls, "_rbac_context_field", matching_fields[0])
        elif len(matching_fields) == 0:
            logging.error(f"No matching RbacContext fields. {cls}")
            raise Exception(
                "Subclasses MUST either have an RbacContext field or override " \
                "the rbac_context method.")
        else:
            logging.error(f"Ambiguous RbacContext fields. {cls}")
            raise Exception(
                "Subclasses with more than one RbacContext field MUST override " \
                "the rbac_context method.")

    def rbac_context(self):
        return self._rbac_context_field.as_rbac_context


class RbacModel(AccessControlledModel):
    class Meta:
        abstract = True

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

    context = models.ForeignKey(Context, null=True, on_delete=models.SET_NULL)

    def rbac_context(self):
        return self.context.get()

    def set_as_context(self, context_obj: RbacContext):
        self.context = context_obj.as_rbac_context


class Role(RbacModel):
    definition = JSONField(null=False)

    # Required by AccessControlled
    resource_type = ResourceType(
        "rbac.Role", "Role", "A Role definition as a JSON resource."
    )

    @property
    def as_policy(self):
        return json_loads_policy(self.definition_json)


class RoleAssignment(RbacModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    resource_type = ResourceType(
        "rbac.RoleAssignment",
        "RoleAssignment",
        "The assignment of an rbac.Role to a User.",
    )


#TODO Figure out how to support custom User models
UserResourceType = ResourceType(
    "rbac.User",
    "User",
    "A resource representing a User.",
)
