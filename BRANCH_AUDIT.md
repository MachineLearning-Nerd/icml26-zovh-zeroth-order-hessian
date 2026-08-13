# Branch audit

## Final published state

| Branch | Role | State |
|---|---|---|
| main | Clean publication branch | Current branch; contains the bounded audit, README, gate, and attribution-normalized history |
| master | Legacy branch | Deleted after main became the default branch |

No orx or orx-* branch was present in the inspected repository. The original snapshot had one branch, master, and one initial commit:

~~~text
d3cbb95aadb31e9ec130c9efe07e2576f49cb324
nEQYu4ndGA ZoVH: 3/6 claims VERIFIED (6 pts, honest)
~~~

That legacy commit used a local DineshAI <dinesh@local> identity and included a Claude co-author trailer. The published history was rewritten as an explicit attribution cleanup so reachable commits use the GitHub identity for MachineLearning-Nerd and no longer contain that trailer. The rewrite changes commit IDs but not the repository’s paper snapshot.

The remote branch, default-branch setting, deleted legacy branch, tip commit, and commit author/committer identities were checked after publication. The migration tip at that readback was:

~~~text
1d3e84b34386ce82eae6edd07a01f1674c70d9ba
~~~

This branch-audit update is a documentation-only descendant of that verified migration tip. The final descendant is checked again after it is pushed; its author and committer use the same MachineLearning-Nerd identity.
