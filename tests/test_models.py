import factory
from django.db import connection, models
from django.db.models.base import ModelBase
from django.test import TestCase
from faker import Faker
from scoped_rbac.models import AccessControlled, Context, RbacContext, Role, RoleAssignment
from scoped_rbac.registry import RbacRegistry
from tests.models import ExampleRbacContext


class RbacContextTestCase(TestCase):
    """
    Verify that models that subclass RbacContext automatically create an associated
    Context model instance on creation.
    """

    def test_simple_creation(self):
        fake = Faker()
        example = ExampleRbacContext(
            name=fake.pystr(min_chars=1, max_chars=128)
        )
        example.save()
        assert example.rbac_context != None
        assert isinstance(example.rbac_context, Context)


class AccessControlledTestCase(TestCase):
    def test_registration_of_resource_types(self):
        assert Role.resource_type in RbacRegistry.known_resource_types()
