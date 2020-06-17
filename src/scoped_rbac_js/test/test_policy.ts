import test from 'ava';
import rbac from '../src/scoped-rbac';

const permissionOne = { "action": "GET", "resource_type": "One" };
const permissionTwo = { "action": "GET", "resource_type": "Two" };
const permissionSuperUserOnly = {
  "action": "NEVER", "resource_type": "shouldn't matter" };

function policyFor(context: string, jsonPolicy: rbac.RootPolicy) {
  const rootPolicy = new rbac.RootPolicy();
  rootPolicy.addJsonPolicyForContext(jsonPolicy, context);
  return rootPolicy;
}

test('empty policy', t => {
  let policy = policyFor("a", "{}")
  t.false(policy.shouldAllow(permissionOne, "a"));
  t.false(policy.shouldAllow(permissionOne, "b"));
  t.false(policy.shouldAllow(permissionSuperUserOnly, "a"));
  policy = policyFor("a", "[]")
  t.false(policy.shouldAllow(permissionOne, "a"));
  t.false(policy.shouldAllow(permissionOne, "b"));
  t.false(policy.shouldAllow(permissionSuperUserOnly, "a"));
  t.fail();
});
