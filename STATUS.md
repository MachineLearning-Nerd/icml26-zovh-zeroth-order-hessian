# ZoVH Zeroth-Order Hessian — audit status

Paper: [Revisiting Zeroth-Order Hessian Approximation: A Single-Step Policy Optimization Lens](https://arxiv.org/abs/2605.30960)
Authors: Junbin Qiu, Zhaowei Hong, Renzhe Xu, Yao Shu
OpenReview: [nEQYu4ndGA](https://openreview.net/forum?id=nEQYu4ndGA)

## Verdict

**INCONCLUSIVE — 0/6 paper-level claims independently verified.**

The repository contains four bounded, deterministic toy diagnostics. Three pass and one is negative. C5 and C6 are not run.

| Claim | Status | What the repository actually checks |
|---|---|---|
| C1 — Propositions 3.2/3.3 | ALGEBRAIC_FINITE_PROXY | Shared finite directions compare the identity-corrected and rank-one forms on a quadratic. |
| C2 — Theorem 4.6 | FINITE_ANALYTIC_PROXY | Finite baseline-difference scaling and convergence to analytic quadratic/quartic smoothed Hessians. |
| C3 — Theorems 4.7/4.8 | FINITE_BIAS_VARIANCE_PROXY | Finite baseline concentration, MSE decrease with K, and quartic smoothing-bias trend. |
| C4 — Figure 2 | HONEST_NEGATIVE | The bare single-batch estimator loses to central differences in one fixed Styblinski-Tang diagnostic. |
| C5 — MNIST attack | NOT_REPRODUCED | No MNIST data, attack, or comparison is present. |
| C6 — synthetic optimization speedup | NOT_REPRODUCED | No full optimizer, query reuse, inverse-Hessian/product estimator, or speedup run is present. |

The passing diagnostics are proxies, not theorem proofs. In particular, this repository does not implement the official query-reuse history buffer or the complete ZoVH system described in the paper.

## Reproduce the audit

~~~bash
python3 repro/src/verify.py
python3 repro/src/finalize_gate.py
~~~

Raw measurements are in [outputs/diagnostics.json](outputs/diagnostics.json); the publication interpretation is in [outputs/gate.json](outputs/gate.json) and [publication_gate.json](publication_gate.json).
