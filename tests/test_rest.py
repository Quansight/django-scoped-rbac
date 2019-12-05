from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ContextTests(APITestCase):
    def test_get_contexts(self):
        response = self.client.get(reverse('context-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_(self):
        response = self.client.post()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class RoleTests(APITestCase):
    def test_get_roles(self):
        response = self.client.get(reverse('role-list'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_post_(self):
        response = self.client.post()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class RoleAssignmentTests(APITestCase):
    def test_get_role_assignments(self):
        response = self.client.get(reverse('roleassignment-list'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_post_(self):
        response = self.client.post()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
