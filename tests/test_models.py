from django.contrib.auth.models import User
from django.test import TestCase
from faker import Faker
from scoped_rbac.models import Context, Role, RoleAssignment
from scoped_rbac.registry import RbacRegistry
from tests.models import ExampleRbacContext
import pytest


class RbacContextTestCase(TestCase):
    """
    Verify that models that subclass RbacContext automatically create an associated
    Context model instance on creation.
    """

    def test_simple_creation(self):
        fake = Faker()
        example = ExampleRbacContext(name=fake.pystr(min_chars=1, max_chars=128))
        example.save()
        assert example.as_rbac_context is not None
        assert isinstance(example.as_rbac_context, Context)


class AccessControlledTestCase(TestCase):
    def test_registration_of_resource_types(self):
        for resource_type in (
            Role.resource_type,
            RoleAssignment.resource_type,
            ExampleRbacContext.resource_type,
        ):
            assert resource_type in RbacRegistry.known_resource_types()
