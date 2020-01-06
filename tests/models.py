from django.db import models
from scoped_rbac.models import RbacContext, AccessControlled


class ScopedRbacModel(models.Model):
    """Mixin class for models used in testing."""

    class Meta:
        app_label = "tests"
        abstract = True

#project
# class ExampleRbacContext(ScopedRbacModel, RbacContext):
#     name = models.CharField(max_length=128)
class ExampleProject(ScopedRbacModel, RbacContext):
    name = models.CharField(max_length=128)

#blog associate with Project
#blog is AccessControlled, must be properly enforced. only allowed what you want to allow based on the roles a user has
#project is rbac context

# A project is an rbac context test model. A blog is associated with a project and is access controlled. The tests verify the test resources can be created and that their access is allowed or denied based on what roles the user has been assigned for that project, e.g. a user with a role assignment for the author role can create and edit a blog entry belonging to that project, but can't do the same for other projects.

class ExampleBlog(ScopedRbacModel, AccessControlled):
    name = models.CharField(max_length=128)
    # project = models.ForeignKey(on_delete=models.CASCADE)
    # resource_type =

# class ExampleRole()
# Do we need an role for testing, an 'author' vs. 'non-author'?
