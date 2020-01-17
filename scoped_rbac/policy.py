"""
RBAC Policies, with stubbed-out support for conditional expressions.
"""

from collections import namedtuple


Permission = namedtuple("Permission", "action, resource_type")


class Policy(object):
    def should_allow(self, permission, context_id, resource=None):
        """
        No actions are allowed by default.
        """
        return False

    def sum_with(self, other_policy):
        """
        Return a Policy representing the result of combining two Policy instances.
        """
        if isinstance(other_policy, ZeroPolicy):
            return self
        if isinstance(other_policy, PolicyList) or isinstance(
            other_policy, RecursivePolicyMap
        ):
            return other_policy.do_sum_with(self)
        return self.do_sum_with(other_policy)

    def do_sum_with(self, other_policy):
        new_policy = PolicyList()
        new_policy.sum_with(self)
        new_policy.sum_with(other_policy)
        return new_policy

    def __repr__(self):
        return "Policy)"


class ZeroPolicy(Policy):
    """
    Useful as a terminal object to implement simple `sum_with` logic.
    """

    def do_sum_with(self, other_policy):
        return other_policy

    def __repr__(self):
        return "ZeroPolicy"


class AllowedPolicy(Policy):
    def should_allow(self, permission, context_id, resource=None):
        return True

    def __repr__(self):
        return "AllowedPolicy"


class ExpressionPolicy(Policy):
    """
    Expression policies are initialized with a `dict` detailing the parameters
    to use in evaluating the expression to determine whether the policy
    conditions are met.
    """

    def __init__(self, expression):
        self.expression = expression

    def evaluate(self, permission, context_id, resource=None):
        raise "Not implemented"

    def should_allow(self, permission, context_id, resource=None):
        return self.evaluate(self, permission, context_id, resource)


class PolicyList(Policy):
    """
    A list of peer policies.
    """

    def __init__(self):
        self.policies = list()

    def do_sum_with(self, other_policy):
        if isinstance(other_policy, PolicyList):
            self.policies.extend(other_policy.policies)
        elif isinstance(other_policy, RecursivePolicyMap):
            return other_policy.do_sum_with(self)
        else:
            self.policies.append(other_policy)
        return self

    def should_allow(self, permission, context_id, resource=None):
        """
        Will return True if _any_ policy contained in the list of policies returns True.
        """
        for policy in self.policies:
            if policy.should_allow(permission, context_id, resource):
                return True
        return False

    def __repr__(self):
        body = ", ".join(self.policies)
        return "[" + body + "]"


class RecursivePolicyMap(Policy):
    """
    A recursively constructed policy of policies. The root instance is keyed by
    context_id.  The child instances are keyed by action. The grand-child instances are
    keyed by resource_type.
    """

    def __init__(self):
        self.policies = dict()
        self.peer_policies = PolicyList()

    def do_sum_with(self, other_policy):
        if isinstance(other_policy, RecursivePolicyMap):
            self.recursive_sum_with(other_policy)
        else:
            self.peer_policies.sum_with(other_policy)
        return self

    def recursive_sum_with(self, other_policy):
        for k, v in other_policy.policies.items():
            current_policy = self.policies.get(k, ZeroPolicy())
            self.policies[k] = current_policy.sum_with(v)

    def should_allow(self, permission, context_id, resource=None):
        """
        Will return true if any peer policies or policies along the path returns True.
        """
        return self.do_should_allow(
            [context_id, permission.action, permission.resource_type],
            permission,
            context_id,
            resource,
        )

    def do_should_allow(self, path, permission, context_id, resource):
        if self.peer_policies.should_allow(permission, context_id, resource):
            return True
        effective_policy = self.policies.get(path[0], ZeroPolicy())
        if isinstance(effective_policy, RecursivePolicyMap):
            return effective_policy.do_should_allow(
                path[1:], permission, context_id, resource
            )
        return effective_policy.should_allow(permission, context_id, resource)

    def add(self, policy, *args):
        key = args[0]
        current_policy = self.policies.get(key, ZeroPolicy())
        if len(args) == 1:
            self.policies[key] = current_policy.sum_with(policy)
        else:
            if isinstance(current_policy, RecursivePolicyMap):
                current_policy.add(policy, *args[1:])
            else:
                new_recursive_policy = RecursivePolicyMap()
                new_recursive_policy.sum_with(current_policy)
                new_recursive_policy.add(policy, *args[1:])
                self.policies[key] = new_recursive_policy

    def __repr__(self):
        return str(self.policies) + ", " + str(self.peer_policies)


ALLOWED = AllowedPolicy()
NOT_ALLOWED = Policy()
