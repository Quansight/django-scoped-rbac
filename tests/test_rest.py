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


@pytest.fixture()
def superuser(transactional_db):
    fake = Faker()
    name = fake.pystr(min_chars=10, max_chars=20)
    email = f"{name}@example.com"
    passwd = fake.pystr(min_chars=12, max_chars=20)
    superuser = User.objects.create_superuser(name, email, passwd,)
    superuser.save()
    return TestUser(name, email, passwd, superuser)


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
