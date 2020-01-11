from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from safetydance_django.test import *
from safetydance_django.steps import http_client, http_response
from safetydance_test import scripted_test, Given, When, Then, And
import pytest


@pytest.mark.django_db
@scripted_test
def test_get_contexts():
    Given.http.get(reverse('context-list'))
    Then.http.status_code_is(200)
    And.http.response_json_is({
            "count": 0,
            "next": None,
            "previous": None,
            "results": [],
        })


@pytest.mark.django_db
@scripted_test
def test_create_contexts():
    Given.http.get("/api/")
    Given.http.get(reverse('examplerbaccontext-list'))
    Then.http.status_code_is(200)
    And.http.response_json_is({
            "count": 0,
            "next": None,
            "previous": None,
            "results": [],
        })

    When.http.post(
        reverse("examplerbaccontext-list"),
        {
            "name": "foo",
        },
        format="json")
    Then.http.status_code_is(201)
    print(http_response._headers)
    When.http.get_created()
    Then.http.status_code_is(200)
    And.http.response_json_is({"name": "foo"})
