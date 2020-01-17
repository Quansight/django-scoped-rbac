from rest_framework import permissions
from .models import RbacContext, RoleAssignment
from .policy import ALLOWED, NOT_ALLOWED, Permission, RecursivePolicyMap


DEFAULT_CONTEXT = None


def policy_for(request):
    # TODO figure out caching for this
    if request.user is None:
        return NOT_ALLOWED
    if request.user.is_superuser:
        return ALLOWED
    role_assignments = RoleAssignment.objects.filter(
        user=request.user
    ).prefetch_related("role")
    policy_by_role = dict()
    total_policy = RecursivePolicyMap()
    for role_assignment in role_assignments.all():
        role = role_assignment.role
        if role not in policy_by_role:
            policy_by_role[role] = role.as_policy
        total_policy.add(policy_by_role[role], role_assignment.rbac_context_id)
    return total_policy


def http_action_iri_for(request):
    return f"http.{request.method.lower()}"


class IsAuthorized(permissions.BasePermission):
    """
    Custom permission handling using the `rbac` model.
    """

    def has_object_permission(self, request, view, obj):
        """
        Requires that the object is `AccessControlled`.
        """
        policy = policy_for(request)
        context_id = obj.rbac_context_id
        result = policy.should_allow(
            Permission(http_action_iri_for(request), obj.resource_type.iri),
            context_id,  # TODO this must be a string in context namespace...
            obj,
        )
        return result

    def has_permission(self, request, view):
        """
        Requires the view to be an `AccessControlledView`.
        """
        policy = policy_for(request)
        resource = request.data if request.method in ("PUT", "POST") else None
        result = policy.should_allow(
            Permission(
                http_action_iri_for(request), view.resource_type_iri_for(request)
            ),
            view.context_id_for(request),
            resource,
        )
        return result
