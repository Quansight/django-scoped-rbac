from scoped_rbac.policy import Permission, RecursivePolicyMap
from scoped_rbac.policy_json import json_loads_policy


permission_one = Permission(action="GET", resource_type="One")
permission_two = Permission(action="GET", resource_type="Two")
permission_super_user_only = Permission(action="NEVER", resource_type="shouldn't matter")
permission_action_only = Permission(action="GET", resource_type=None)


def policy_for(context_id, json_policy):
    policy = RecursivePolicyMap()
    if isinstance(json_policy, str):
        json_policy = json_loads_policy(json_policy)
    policy.add(json_policy, context_id)
    return policy

class TestJsonPolicy:
    def test_empty(self):
        policy = policy_for("a", "{}")
        assert not policy.should_allow(permission_one, "a")
        assert not policy.should_allow(permission_one, "b")
        assert not policy.should_allow(permission_super_user_only, "a")
        policy = policy_for("a", "[]")
        assert not policy.should_allow(permission_one, "a")
        assert not policy.should_allow(permission_one, "b")
        assert not policy.should_allow(permission_super_user_only, "a")

    def test_all_allowed(self):
        policy = policy_for("a", "true")
        assert policy.should_allow(permission_one, "a")
        assert policy.should_allow(permission_super_user_only, "a")
        assert not policy.should_allow(permission_one, "b")
        assert not policy.should_allow(permission_super_user_only, "b")

    def test_string_allowed(self):
        policy = policy_for("a", "\"GET\"")
        assert policy.should_allow(permission_one, "a")
        assert not policy.should_allow(permission_super_user_only, "a")
        assert not policy.should_allow(permission_one, "b")
        assert not policy.should_allow(permission_super_user_only, "b")

    def test_list_allowed(self):
        policy = policy_for("a", "[ \"GET\", \"POST\" ]")
        assert policy.should_allow(Permission("GET", "doesn't matter"), "a")
        assert policy.should_allow(Permission("POST", "doesn't matter"), "a")
        assert not policy.should_allow(Permission("DELETE", "doesn't matter"), "a")
        assert not policy.should_allow(Permission("GET", "doesn't matter"), "b")
        assert not policy.should_allow(Permission("POST", "doesn't matter"), "b")
        assert not policy.should_allow(Permission("DELETE", "doesn't matter"), "b")

    def test_with_paths(self):
        policy = policy_for("a",
            """
            {
                "GET.one": "One"
                , "GET.list": [
                    "One"
                    , "Two"
                ]
                , "GET.true": true
            }
            """
        )
        assert policy.should_allow(Permission("GET.one", "One"), "a")
        assert not policy.should_allow(Permission("GET.one", "Two"), "a")
        assert policy.should_allow(Permission("GET.list", "One"), "a")
        assert policy.should_allow(Permission("GET.list", "Two"), "a")
        assert not policy.should_allow(Permission("GET.list", "Three"), "a")
        assert policy.should_allow(Permission("GET.true", "One"), "a")
        assert not policy.should_allow(permission_super_user_only, "a")

        assert not policy.should_allow(Permission("GET.one", "One"), "b")
        assert not policy.should_allow(Permission("GET.one", "Two"), "b")
        assert not policy.should_allow(Permission("GET.list", "One"), "b")
        assert not policy.should_allow(Permission("GET.list", "Two"), "b")
        assert not policy.should_allow(Permission("GET.list", "Three"), "b")
        assert not policy.should_allow(Permission("GET.true", "One"), "b")
        assert not policy.should_allow(permission_super_user_only, "b")
