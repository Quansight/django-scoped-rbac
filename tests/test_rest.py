from dataclasses import dataclass
from django.contrib.auth.models import User
# from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from safetydance_django.test import *
from safetydance_django.steps import http_client, http_response
from safetydance_test import scripted_test, Given, When, Then, And
from scoped_rbac.models import Role
import logging
import pytest


@dataclass
class TestUser:
    username: str
    email: str
    password: str
    instance: object


def create_user(is_super=False):
    fake = Faker()
    name = fake.pystr(min_chars=10, max_chars=20)
    email = f"{name}@example.com"
    passwd = fake.pystr(min_chars=12, max_chars=20)
    if is_super:
        user = User.objects.create_superuser(name, email, passwd,)
    else:
        user = User.objects.create(
                username=name,
                email=email,
                password=passwd,
                is_active=True,
                )
    user.save()
    return TestUser(name, email, passwd, user)


@pytest.fixture()
def superuser(transactional_db):
    # fake = Faker()
    # name = fake.pystr(min_chars=10, max_chars=20)
    # email = f"{name}@example.com"
    # passwd = fake.pystr(min_chars=12, max_chars=20)
    # superuser = User.objects.create_superuser(name, email, passwd,)
    # superuser.save()
    # return TestUser(name, email, passwd, superuser)
    return create_user(is_super=True)

@pytest.fixture()
def editor_user(transactional_db):
    return create_user()


@pytest.fixture()
def not_authorized_user(transactional_db):
    return create_user()


@pytest.mark.django_db
@scripted_test
def test_get_contexts(superuser):
    Given.http.login(username=superuser.username, password=superuser.password)
    When.http.get(reverse("context-list"))
    Then.http.status_code_is(200)
    And.http.response_json_is(
        {"count": 0, "next": None, "previous": None, "results": [],}
    )


@pytest.mark.django_db
@scripted_test
def test_create_contexts(superuser):
    Given.http.force_authenticate(user=superuser.instance)
    When.http.get(reverse("examplerbaccontext-list"))
    Then.http.status_code_is(200)
    And.http.response_json_is(
        {"count": 0, "next": None, "previous": None, "results": [],}
    )

    When.http.post(reverse("examplerbaccontext-list"), {"name": "foo"}, format="json")
    Then.http.status_code_is(201)
    When.http.get_created()
    Then.http.status_code_is(200)
    And.http.response_json_is({"name": "foo"})

    # FIXME delete after testing, add envelope testing
    # When.http.get(reverse("examplerbaccontext-list"))
    # print(http_response.json())
    # print(http_response._headers)
    # raise Exception("just want the trace")


@pytest.mark.django_db
@scripted_test
def test_simple_role_assignment(superuser, editor_user, not_authorized_user):
    fake = Faker()
    context_name = fake.pystr(min_chars=10, max_chars=20)
    editor_user_url = reverse("user-detail", [editor_user.instance.pk])
    logging.info(editor_user_url)

    # Create a context
    Given.http.force_authenticate(user=superuser.instance)
    When.http.post(
            reverse("examplerbaccontext-list"), {"name": context_name}, format="json")
    Then.http.status_code_is(201)
    context_url = http_response["location"]
    logging.info(context_url)

    # Create a role
    When.http.post(
            reverse("role-list"),
            {
                "definition": {
                    "http.POST": [
                        Role.resource_type.iri,
                        ],
                    "http.GET": [
                        Role.resource_type.iri,
                        Role.resource_type.list_iri,
                        ],
                    "http.PUT": [
                        Role.resource_type.iri,
                        ],
                    "http.DELETE": [
                        Role.resource_type.iri,
                        ],
                },
                # TODO add these fields
                # "name": role_name,
                # "description": role_description,
                "rbac_context": context_url,
            },
            format="json",
        )
    logging.info(http_response)
    logging.info(http_response.data)
    Then.http.status_code_is(201)
    role_url = http_response["location"]

    # Assign the role to editor_user
    When.http.post(
            reverse("roleassignments-list"),
            {
                "user": editor_user_url,
                "role": role_url,
                "rbac_context": context_url,
            },
            format="json",
        )
    Then.http.status_code_is(201)

    # Switch to the editor_user
    Given.http.force_authenticate(user=editor_user.instance)

    # Create a protected resource as editor_user
    protected_resource_content = {
            "definition_json": {},
            "rbac_context": context_url,
        },
    When.http.post(reverse("role-list"), protected_resource_content, format="json")
    Then.http.status_code_is(201)
    protected_resource_url = http_response["location"]

    # Get the resource 
    When.http.get(protected_resource_url)
    Then.http.status_code_is(200)
    And.http.response_json_is(protected_resource_content)

    # Update the resource
    updated_content = {
            "definition_json": {
                "GET": True,
                },
            "rbac_context": context_url,
        }
    When.http.put(protected_resource_url, updated_content)
    Then.http.status_code_is(200)
    When.http.get(protected_resourceurl)
    Then.http.status_code_is(200)
    And.http.response_json_is(updated_content)

    # Get the resource list as the editor_user
    When.http.get(reverse("role-list"))
    Then.http.status_code_is(200)

    # Switch to the not_authorized_user
    Given.http.force_authenticate(user=not_authorized_user.instance)

    # Get the resource list as the not_authorized_user
    # check that it failed
    When.http.get(reverse("role-list"))
    Then.http.status_code_is(403)

    # Get the resource as the not_authorized_user
    # check that it failed
    When.http.get(protected_resource_url)
    Then.http.status_code_is(403)

    # Update the resource
    # check that it failed
    When.http.put(protected_resource_url, {})
    Then.http.status_code_is(403)

    # Delete the resource
    # check that it failed
    When.http.delete(protected_resource_url)
    Then.http.status_code_is(403)

    # Create a resource
    # check that it failed
    When.http.post(reverse("role-list"), {}, format="json")
    Then.http.status_code_is(403)

    # Switch to the editor_user
    # delete the resource
    Given.http.force_authenticate(user=editor_user.instance)
    And.http.get(protected_resource_content)
    And.http.delete(protected_resource_url)
    Then.status_code_is(200)

    # double check it's gone
    When.http.get(protected_resource_url)
    Then.http.status_code_is(404)
