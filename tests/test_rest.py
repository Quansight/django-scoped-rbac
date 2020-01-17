from dataclasses import dataclass
from django.contrib.auth.models import User
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from safetydance_django.test import *
from safetydance_django.steps import http_client, http_response
from safetydance_test import scripted_test, Given, When, Then, And
from scoped_rbac.models import Context, Role, RoleAssignment
from tests.models import ExampleRbacContext
import json
import pytest


@dataclass
class UserData:
    username: str
    email: str
    password: str
    instance: object


def create_test_user(superuser=False):
    fake = Faker()
    name = fake.pystr(min_chars=10, max_chars=20)
    email = f"{name}@example.com"
    password = fake.pystr(min_chars=12, max_chars=20)
    if not superuser:
        user = User.objects.create_user(name, email, password,)
    else:
        user = User.objects.create_superuser(name, email, password,)
    user.save()
    return UserData(name, email, password, user)


def create_role(json_policy_dict: dict, context: Context):
    role = Role.objects.create(definition_json=json.dumps(json_policy_dict),)
    if context is not None:
        role.rbac_context = context
    role.save()
    return role


def create_user_with_roles(role_context_pairs):
    user = create_test_user()
    for role, context in role_context_pairs:
        role_assignment = RoleAssignment.objects.create(user=user.instance, role=role,)
        if context is not None:
            role_assignment.rbac_context = context
        role_assignment.save()
    return user


@pytest.fixture()
def superuser(transactional_db):
    return create_test_user(superuser=True)


@pytest.fixture()
def no_roles_user(transactional_db):
    return create_test_user()


@pytest.fixture()
def roles_for_testing(transactional_db):
    return {
        "context_get_list": create_role(
            {"http.get": [Context.resource_type.iri_as_collection,],}, None
        ),
        "example_rbac_context_get_list": create_role(
            {"http.get": [ExampleRbacContext.resource_type.iri_as_collection,],}, None
        ),
        "example_rbac_context_get_detail": create_role(
            {"http.get": [ExampleRbacContext.resource_type.iri,],}, None
        ),
        "example_rbac_context_post_put_delete": create_role(
            {
                "http.post": [ExampleRbacContext.resource_type.iri,],
                "http.put": [ExampleRbacContext.resource_type.iri,],
                "http.delete": [ExampleRbacContext.resource_type.iri,],
            },
            None,
        ),
    }


@pytest.fixture()
def testing_users(transactional_db, roles_for_testing):
    return {
        "superuser": create_test_user(superuser=True),
        "no_roles_user": create_test_user(),
        "user_context_get_list": create_user_with_roles(
            [(roles_for_testing["context_get_list"], None),]
        ),
        "user_example_rbac_context_get_list": create_user_with_roles(
            [(roles_for_testing["example_rbac_context_get_list"], None),]
        ),
        "user_example_rbac_context_all": create_user_with_roles(
            [
                (roles_for_testing["example_rbac_context_get_list"], None),
                (roles_for_testing["example_rbac_context_get_detail"], None),
                (roles_for_testing["example_rbac_context_post_put_delete"], None),
            ]
        ),
    }


@pytest.mark.django_db
@scripted_test
def test_get_contexts(superuser):
    Given.http.force_authenticate(superuser.instance)
    When.http.get(reverse("context-list"))
    Then.http.status_code_is(200)
    And.http.response_json_is(
        {"count": 0, "next": None, "previous": None, "results": [],}
    )


@pytest.mark.parametrize(
    "username, get_listing_allowed, post_allowed, get_detail_allowed",
    (
        ("superuser", True, True, True),
        ("no_roles_user", False, False, False),
        ("user_example_rbac_context_get_list", True, False, False),
        ("user_example_rbac_context_all", True, True, True),
    ),
)
@pytest.mark.django_db
@scripted_test
def test_create_contexts(
    testing_users, username, get_listing_allowed, post_allowed, get_detail_allowed
):
    user = testing_users[username]
    Given.http.force_authenticate(user=user.instance)
    When.http.get(reverse("examplerbaccontext-list"))
    if get_listing_allowed:
        Then.http.status_code_is(200)
        And.http.response_json_is(
            {"count": 0, "next": None, "previous": None, "results": [],}
        )
    else:
        Then.http.status_code_is(403)

    When.http.post(reverse("examplerbaccontext-list"), {"name": "foo"}, format="json")
    if post_allowed:
        Then.http.status_code_is(201)
        When.http.get_created()
        if get_detail_allowed:
            Then.http.status_code_is(200)
            And.http.response_json_is({"name": "foo"})
        else:
            Then.http.status_code_is(403)
    else:
        Then.http.status_code_is(403)
