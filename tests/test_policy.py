from scoped_rbac.policy import (
    AllowedPolicy,
    Permission,
    Policy,
    PolicyList,
    RecursivePolicyMap,
    ZeroPolicy,
)


permission_one = Permission(action="GET", resource_type="One")
permission_two = Permission(action="GET", resource_type="Two")
permission_never_used = Permission(action="NEVER", resource_type="shouldn't matter")
permission_action_only = Permission(action="GET", resource_type=None)


class TestPolicyList:
    """
    TODO test with conditionals.
    """

    def test_empty_list(self):
        policy = PolicyList()
        assert policy.should_allow(permission_one, "a") is False

    def test_non_empty_list(self):
        policy = ZeroPolicy().sum_with(AllowedPolicy())
        assert policy.should_allow(permission_one, "a") is True

        policy = Policy().sum_with(policy)
        assert policy.should_allow(permission_one, "a") is True


class TestRecursivePolicyMap:
    def test_empty(self):
        policy = RecursivePolicyMap()
        assert policy.should_allow(permission_one, "a") is False

    def test_with_paths(self):
        root_policy = RecursivePolicyMap()
        root_policy.add(AllowedPolicy(), "a", permission_action_only.action)
        root_policy.add(AllowedPolicy(), "b", *permission_one)
        root_policy.add(AllowedPolicy(), "c", *permission_one)
        root_policy.add(AllowedPolicy(), "c", *permission_two)
        root_policy.add(AllowedPolicy(), "d")

        assert root_policy.should_allow(permission_one, "a") is True
        assert root_policy.should_allow(permission_two, "a") is True
        assert root_policy.should_allow(permission_action_only, "a") is True
        assert root_policy.should_allow(permission_never_used, "a") is False

        assert root_policy.should_allow(permission_one, "b") is True
        assert root_policy.should_allow(permission_two, "b") is False
        assert root_policy.should_allow(permission_action_only, "b") is False
        assert root_policy.should_allow(permission_never_used, "b") is False

        assert root_policy.should_allow(permission_one, "c") is True
        assert root_policy.should_allow(permission_two, "c") is True
        assert root_policy.should_allow(permission_action_only, "c") is False
        assert root_policy.should_allow(permission_never_used, "c") is False

        assert root_policy.should_allow(permission_one, "d") is True
        assert root_policy.should_allow(permission_two, "d") is True
        assert root_policy.should_allow(permission_action_only, "d") is True
        assert root_policy.should_allow(permission_never_used, "d") is True
