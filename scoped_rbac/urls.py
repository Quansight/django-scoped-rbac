from rest_framework.routers import DefaultRouter
from . import rest

router = DefaultRouter()
router.register(r"contexts", rest.ContextViewSet)
router.register(r"role-assignments", rest.RoleAssignmentViewSet)
router.register(r"roles", rest.RoleViewSet)
router.register(r"users", rest.UserViewSet)
# router.register(r"content-type", rest.ContentTypeViewSet)
