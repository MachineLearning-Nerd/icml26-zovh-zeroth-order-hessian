# Source and paper audit

## Paper identity

- Title: Revisiting Zeroth-Order Hessian Approximation: A Single-Step Policy Optimization Lens
- Authors: Junbin Qiu, Zhaowei Hong, Renzhe Xu, and Yao Shu
- arXiv: 2605.30960, version 1, submitted 2026-05-29
- OpenReview submission: nEQYu4ndGA
- Official author code: https://github.com/Qjbtiger/ZoVH
- Paper links:
  - https://arxiv.org/abs/2605.30960
  - https://openreview.net/forum?id=nEQYu4ndGA

The pinned paper record and cached docs/paper.html and docs/paper.txt provide
the claim labels and section references. They are reference material, not a
substitute for the official implementation or data.

## What was inspected

The checkout contains finite implementations of two Hessian forms, smoothed
references, an optimal-baseline diagnostic, central differences, the existing
C1–C4 raw diagnostics, and the previous branch audit. The standardized ledger
reads those existing outputs.

This audit does not claim to run the official author code.

## Missing paper-level evidence

- Variance-reduced ZoVH implementation and query-reuse history buffer.
- Inverse-Hessian and inverse-Hessian-gradient-product estimators.
- Curvature-aware optimizer and convergence curves.
- Complete Figure 2 protocol and equal-budget comparisons.
- MNIST black-box attack and synthetic speedup experiments.
- LLM fine-tuning and formal proof verification.

These absences explain C5 and C6 NOT_REPRODUCED and why all six
paper_claim_reproduced fields are false.

## Clean-room boundary

The repository documents independently written finite toy diagnostics. It
should be cited as an independent bounded audit, not represented as an author
release or author-endorsed reproduction.
