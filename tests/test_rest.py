from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from safetydance_django.test import *
from safetydance_test import scripted_test, Given, When, Then, And
import pytest


@pytest.mark.django_db
@scripted_test
def test_get_contexts():
    Given.http.get(reverse('context-list'))
    Then.http.status_code_is(200)
    And.http.response_json_is([])

    
