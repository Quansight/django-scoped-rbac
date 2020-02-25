import json
from .policy import RecursivePolicyMap, RootPolicyMap, ALLOWED, NOT_ALLOWED


def json_loads_policy(policy_json):
    return policy_from_json(json.loads(policy_json))


def policy_from_list(policy_list):
    if len(policy_list) == 0:
        return NOT_ALLOWED
    policy = RecursivePolicyMap()
    for item in policy_list:
        if isinstance(item, str):
            policy.add(ALLOWED, item)
        else:
            raise "Conditional expressions aren't supported, yet"
    return policy


def policy_from_json(policy_json):
    if policy_json is True:
        return ALLOWED
    if policy_json is False:
        return NOT_ALLOWED
    if isinstance(policy_json, str):
        policy = RecursivePolicyMap()
        policy.add(ALLOWED, policy_json)
        return policy
    if isinstance(policy_json, list):
        return policy_from_list(policy_json)
    if isinstance(policy_json, dict):
        policy = RecursivePolicyMap()
        for key, sub_policy in policy_json.items():
            policy.add(policy_from_json(sub_policy), key)
        return policy
    raise "Conditional expressions aren't supported, yet"
