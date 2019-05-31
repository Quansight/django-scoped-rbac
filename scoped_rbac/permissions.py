from rest_framework import permissions
from .models import RoleAssignment
from .policy import ALLOWED, RecursivePolicyMap


def policy_for(request):
    # TODO figure out caching for this
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
        total_policy.add(policy_by_role[role], role_assignment.context.id)
    return total_policy


def http_action_iri_for(request):
    return f"http.{request.method}"


class IsAuthorized(permissions.BasePermission):
    """
    Custom permission handling using the `rbac` model.
    """

    def has_object_permission(self, request, view, obj):
        """
        Requires that the object is `AccessControlled`.
        """
        policy = policy_for(request)
        return policy.should_allow(
            obj.rbac_context.id,
            http_action_iri_for(request),
            obj.resource_type.iri,
            obj,
        )

    def has_permission(self, request, view):
        """
        Requires the view to be an `AccessControlledView`.
        """
        policy = policy_for(request)
        resource = request.data if request.method in ("PUT", "POST") else None
        return policy.should_allow(
            view.context_id_for(request),
            http_action_iri_for(request),
            view.resource_type_iri_for(request),
            resource,
        )
