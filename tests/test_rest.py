from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from scoped_rbac.registry import ResourceType
from tests.models import ExampleProject, ExampleBlog

#create from test models an ExampleProject() and make sure I can get the queryset
class ContextTests(APITestCase):
    def test_get_contexts(self):
        proj = ExampleProject.objects.create(name='proj1')
        assert isinstance(proj, ExampleProject)
        blog = ExampleBlog.objects.create(name='blog1', rbac_context=proj.rbac_context)
        response = self.client.get(reverse('context-list'))
        # response = self.client.get('/projects')
        # response = self.client.get(reverse('exampleProject-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.content)
        # import pdb; pdb.set_trace()

    def test_post_contexts(self):
        #client self.client.post(edit, json for data )
        post_response = self.client.post(reverse('context-list'), data={'object_id':1,'content_type':10}, format='json')
        # import pdb; pdb.set_trace()
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        get_response = self.client.get(reverse('context-list'))
        import pdb; pdb.set_trace()




# class RoleTests(APITestCase):
#     def test_get_roles(self):
#         response = self.client.get(reverse('role-list'))
#         self.assertEquals(response.status_code, status.HTTP_200_OK)
#     #create a json object to pass as context
#     def test_post_roles(self):
#         role = {"definition_json":"definition test text",
#                 "resource_type": ['role','foo','bar']}
#         response = self.client.post(reverse('role-list'), context=role, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#
# class RoleAssignmentTests(APITestCase):
#     def test_get_role_assignments(self):
#         response = self.client.get(reverse('roleassignment-list'))
#         self.assertEquals(response.status_code, status.HTTP_200_OK)
#
#     def test_post_role_assignments(self):
#         roleAssignment = {'user': 'me',
#                           'role': 'roleassignment',
#                           'resource_type': 'foo'
#                           }
#         response = self.client.post(reverse('roleassignment-list'), context=roleAssignment, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
