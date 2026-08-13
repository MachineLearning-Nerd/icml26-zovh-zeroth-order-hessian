# ICML 2026 — ZoVH Zeroth-Order Hessian

Independent evidence audit for **“Revisiting Zeroth-Order Hessian Approximation: A Single-Step Policy Optimization Lens”** by Junbin Qiu, Zhaowei Hong, Renzhe Xu, and Yao Shu.

> **Status: INCONCLUSIVE.** Three of four bounded finite toy diagnostics pass. **0/6 paper-level claims are independently verified.** One finite diagnostic is negative; the MNIST attack and synthetic optimization claims were not run.

## Paper

- arXiv: [2605.30960](https://arxiv.org/abs/2605.30960) (v1, submitted 2026-05-29)
- OpenReview: [nEQYu4ndGA](https://openreview.net/forum?id=nEQYu4ndGA)
- Paper HTML snapshot: [docs/paper.html](docs/paper.html)
- Official author code: [Qjbtiger/ZoVH](https://github.com/Qjbtiger/ZoVH)

The paper reframes Gaussian zeroth-order Hessian estimation as the Hessian of a smoothed single-step policy-optimization objective. It then proposes ZoVH, a variance-reduced suite built around an averaged variance-optimal baseline and a history buffer that reuses past function queries. The full paper also develops regularized inverse-Hessian and inverse-Hessian-gradient-product estimators, a curvature-aware ZOO optimizer, convergence results, and experiments on synthetic objectives, a CNN/MNIST setting, a black-box MNIST attack, and LLM fine-tuning.

This repository is a small clean-room diagnostic of selected estimator identities. It is not a port of the official implementation.

## Evidence summary

| ID | Paper claim or experiment | Evidence produced here | Status |
|---|---|---|---|
| C1 | Propositions 3.2 and 3.3: identity-corrected and rank-one Gaussian forms | Shared finite directions on a deterministic quadratic; compare both matrices and their analytic Hessian | ALGEBRAIC_FINITE_PROXY |
| C2 | Theorem 4.6: unbiasedness of the smoothed Hessian estimator | Finite baseline-difference scaling plus quadratic/quartic analytic smoothed-Hessian convergence | FINITE_ANALYTIC_PROXY |
| C3 | Theorems 4.7 and 4.8: optimal baseline and bias-variance behavior | Finite dimension trend for b*, MSE across K, and quartic smoothing-bias trend | FINITE_BIAS_VARIANCE_PROXY |
| C4 | Figure 2 accuracy comparison | Bare Proposition 3.2 estimator versus central differences on Styblinski-Tang at one fixed setting | HONEST_NEGATIVE |
| C5 | Section 6.3 MNIST black-box adversarial attack | No data, attack implementation, or reported runs | NOT_REPRODUCED |
| C6 | Section 6.2 synthetic curvature-aware ZOO speedup | No optimizer, convergence curves, or speedup runs | NOT_REPRODUCED |

The finite diagnostics are intentionally narrower than the paper. A passing proxy means only that the recorded finite computation behaved as expected under its stated toy setup; it does not convert a theorem or empirical result into a reproduced claim.

## How each result is produced

Run:

~~~bash
python3 repro/src/verify.py
python3 repro/src/finalize_gate.py
~~~

The first command writes raw measurements to [outputs/diagnostics.json](outputs/diagnostics.json) and [outputs/verdict.json](outputs/verdict.json). The second command writes the six-claim publication report to [outputs/gate.json](outputs/gate.json) and [publication_gate.json](publication_gate.json).

### C1 — estimator forms

verify.py creates a positive-semidefinite quadratic, samples one shared Gaussian direction matrix, estimates F_mu, and evaluates both the identity-corrected form (f(theta + mu u) - b)(u u^T - I)/mu² and the rank-one form (f(theta + mu u) - F_mu)u u^T/mu².

It records each error against the known quadratic Hessian and the norm of the difference between the two finite matrices. This is an algebraic finite proxy, not a general proof.

### C2 — unbiasedness proxy

The verifier evaluates the identity-corrected estimator with baseline 0 and with a Monte Carlo estimate of F_mu on increasing shared sample sizes. It then estimates the smoothed Hessian on a quadratic and a quartic and compares against their analytic expectations. The result is labeled a finite analytic proxy because no stochastic function noise or theorem-level assumptions are exercised.

### C3 — bias-variance proxy

The verifier:

1. estimates the paper’s constant variance-optimal baseline b* and compares it with F_mu for dimensions 3, 6, 12, and 24;
2. measures estimator MSE for K in 20, 50, 100, and 200 on a quadratic;
3. measures quartic smoothing bias for mu in 0.05, 0.1, 0.2, and 0.4 against a loose toy bound.

These are finite trends only. They do not validate the paper’s constants, assumptions, query reuse, or stochastic-noise model.

### C4 — negative accuracy diagnostic

The bare single-batch Proposition 3.2 estimator is evaluated on Styblinski-Tang with K=200 and mu=0.1, then compared with a central-difference reference under the fixed settings in the script. The observed bare-estimator error is larger. This is an honest negative for this limited diagnostic, not a claim that the paper’s complete Figure 2 protocol was reproduced: query reuse, control variates, competing estimators, and all reported settings are absent.

### C5 and C6 — not run

There is no MNIST data pipeline or black-box attack for C5. There is no implementation of the paper’s full ZoVH optimizer, inverse-Hessian/product estimators, query-reuse history buffer, convergence evaluation, or speedup comparison for C6. Therefore both remain NOT_REPRODUCED, rather than being inferred from the toy diagnostics.

## Repository map

- [repro/src/core.py](repro/src/core.py) — finite implementations of the two Hessian forms, smoothed references, optimal-baseline diagnostic, and central differences.
- [repro/src/verify.py](repro/src/verify.py) — bounded C1–C4 diagnostics and raw JSON output.
- [repro/src/finalize_gate.py](repro/src/finalize_gate.py) — converts raw diagnostics into the six-claim publication gate.
- [outputs/](outputs) — generated measurements and gate reports.
- [docs/paper.html](docs/paper.html), [docs/paper.txt](docs/paper.txt) — pinned paper snapshots used during the audit.
- [.trackio/logbook/](.trackio/logbook) — a readable experiment log mirroring the same scope and verdict.
- [STATUS.md](STATUS.md), [GATE_READY.md](GATE_READY.md), [BRANCH_AUDIT.md](BRANCH_AUDIT.md) — status, gate interpretation, and branch history.

## Branches and attribution

The cleaned publication branch is main. The original snapshot was on master; it contained one initial commit and no orx or orx-* branch. The old branch was removed after main became the default branch. See [BRANCH_AUDIT.md](BRANCH_AUDIT.md) for the exact migration record.

Approved cleanup commits are attributed to **MachineLearning-Nerd**. No author, paper, or official-code contribution is implied by that attribution.

## Citation

~~~bibtex
@inproceedings{qiu2026zovh,
  title     = {Revisiting Zeroth-Order Hessian Approximation: A Single-Step Policy Optimization Lens},
  author    = {Qiu, Junbin and Hong, Zhaowei and Xu, Renzhe and Shu, Yao},
  booktitle = {Proceedings of the 43rd International Conference on Machine Learning},
  year      = {2026},
  eprint    = {2605.30960},
  archivePrefix = {arXiv},
  url       = {https://arxiv.org/abs/2605.30960}
}
~~~

## Thank you

Thank you to Junbin Qiu, Zhaowei Hong, Renzhe Xu, and Yao Shu for making the paper, derivations, empirical protocol, and official code available. This audit is intended as a transparent, limited reproduction record that makes clear what was checked, what was not checked, and where the clean-room implementation differs from the full ZoVH system.
