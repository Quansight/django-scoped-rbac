from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ContextTests(APITestCase):
    def test_get_contexts(self):
        response = self.client.get(reverse('context-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
