from dataclasses import dataclass
from django.contrib.auth.models import User
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from safetydance_django.test import *
from safetydance_django.steps import http_client, http_response
from safetydance_test import scripted_test, Given, When, Then, And
import pytest


@dataclass
class TestUser:
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
    return TestUser(name, email, password, user)


@pytest.fixture()
def superuser(transactional_db):
    return create_test_user(superuser=True)


@pytest.fixture()
def no_roles_user(transactional_db):
    return create_test_user()


@pytest.fixture()
def testing_users(transactional_db, superuser, no_roles_user):
    return {
        "superuser": superuser,
        "no_roles_user": no_roles_user,
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
    (("superuser", True, True, True), ("no_roles_user", False, False, False),),
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
