# Branch and commit audit

## Normalization

- Source tip before standardization:
  f39b869df88639cd2028cee2a95444f4b74319c3.
- The source repository exposed master; the live repository now exposes only
  main.
- The source had no experiment or paper-version branches in scope.
- Recovery bundle SHA-256:
  3817d3b55118ea1cb61f819d7898d4634339e8a328effbe7761c5bfe33b1b978.
- The recovery bundle preserves the complete pre-normalization history.

## Current branch policy

- main is the canonical paper metadata, evidence, and verifier branch.
- New evidence should use a descriptive audit/... branch and record the paper
  version, command, inputs, outputs, controls, and limitations before merging.
- The cached paper snapshots are reference material; arXiv 2605.30960v1 is
  authoritative for version-sensitive claims in this audit.

## Attribution policy

All reachable commits in the published history use:

MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>

The old master branch name and earlier identity are retained only in the
recovery bundle and history notes, not as live branch or commit metadata.
