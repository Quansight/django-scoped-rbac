import test from 'ava';
import * as rbac from '../src/scoped-rbac';

const permissionOne = { action: "GET", resourceType: "One" };
const permissionTwo = { action: "GET", resourceType: "Two" };
const permissionSuperUserOnly = { action: "NEVER", resourceType: "shouldn't matter" };

function policyFor(context: string, jsonPolicy: rbac.PolicySource) {
  const rootPolicy = new rbac.RootPolicy();
  rootPolicy.addJsonPolicyForContext(jsonPolicy, context);
  return rootPolicy;
}

test('empty policy', t => {
  let policy = policyFor("a", "{}")
  t.false(policy.shouldAllow(permissionOne, "a", "One"));
  t.false(policy.shouldAllow(permissionOne, "b", "One"));
  t.false(policy.shouldAllow(permissionSuperUserOnly, "a", "One"));
  policy = policyFor("a", "[]")
  t.false(policy.shouldAllow(permissionOne, "a", "One"));
  t.false(policy.shouldAllow(permissionOne, "b", "One"));
  t.false(policy.shouldAllow(permissionSuperUserOnly, "a", "One"));
});
