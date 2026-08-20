# ICML 2026 — ZoVH Zeroth-Order Hessian

Paper-level result: INCONCLUSIVE.

This repository is an independent, bounded clean-room evidence audit of
Revisiting Zeroth-Order Hessian Approximation: A Single-Step Policy
Optimization Lens. It contains small finite diagnostics for selected estimator
identities and toy analytic behavior. It is not a port of the official ZoVH
implementation and does not reproduce the complete optimizer or experiments.

Three of four finite diagnostics pass, one finite diagnostic is an honest
negative, and zero of six complete paper claims are independently verified.
The package may be published as a bounded audit; it must not be presented as
a full reproduction, and it makes no current external score claim.

## Paper

- Title: Revisiting Zeroth-Order Hessian Approximation: A Single-Step Policy Optimization Lens
- Authors: Junbin Qiu, Zhaowei Hong, Renzhe Xu, and Yao Shu
- arXiv: 2605.30960, version 1, submitted 2026-05-29
- Paper HTML: docs/paper.html
- OpenReview: nEQYu4ndGA
- Official author code: https://github.com/Qjbtiger/ZoVH
- Cached source: docs/paper.html and docs/paper.txt

The paper reframes Gaussian zeroth-order Hessian estimation as the Hessian of
a smoothed single-step policy-optimization objective. It proposes variance
reduction with an averaged baseline and query-reuse history buffer, and also
studies inverse-Hessian estimators, a curvature-aware optimizer, convergence,
MNIST attacks, synthetic speedups, and LLM fine-tuning.

## Claim ledger

| ID | Paper target | Local evidence | Status |
| --- | --- | --- | --- |
| C1 | Propositions 3.2 and 3.3 estimator forms | Shared finite Gaussian directions on a quadratic | ALGEBRAIC_FINITE_PROXY |
| C2 | Theorem 4.6 smoothed-Hessian unbiasedness | Finite baseline scaling and analytic quadratic/quartic convergence | FINITE_ANALYTIC_PROXY |
| C3 | Theorems 4.7 and 4.8 baseline and bias-variance behavior | Finite dimension, MSE, and smoothing-bias trends | FINITE_BIAS_VARIANCE_PROXY |
| C4 | Figure 2 accuracy comparison | Bare estimator worse than central differences at one fixed setting | HONEST_NEGATIVE |
| C5 | Section 6.3 MNIST black-box attack | Data and attack pipeline absent | NOT_REPRODUCED |
| C6 | Section 6.2 synthetic curvature-aware ZOO speedup | Optimizer and speedup runs absent | NOT_REPRODUCED |

The statuses describe local evidence, not successful reproduction of the
paper claims. The machine-readable contract is in claims.json, and detailed
production paths are in CLAIM_EVIDENCE.md.

## How each claim is produced

The existing raw diagnostic output is preserved. The publication ledger can be
formatted without running the scientific implementation:

~~~bash
python3 repro/src/finalize_gate.py
python3 verify_final.py
~~~

1. C1 samples shared finite Gaussian directions on a deterministic
   positive-semidefinite quadratic and compares identity-corrected and
   rank-one forms against the analytic Hessian. Their form difference is
   8.746309929968238e-16.
2. C2 checks baseline-difference scaling and analytic quadratic/quartic
   smoothed-Hessian convergence as sample sizes increase. The final recorded
   quadratic and quartic relative errors are 0.0194 and 0.0225.
3. C3 measures finite optimal-baseline concentration, MSE for K in 20, 50,
   100, and 200, and quartic smoothing bias for four smoothing values. MSE
   decreases from 603.182 to 53.729 as K grows.
4. C4 compares the bare single-batch estimator with central differences on
   Styblinski-Tang at K=200 and mu=0.1. The errors are 75.504 and 0.0016, so
   the bounded comparison is negative.
5. C5 has no MNIST data, attack implementation, or reported runs.
6. C6 has no complete ZoVH optimizer, inverse-Hessian/product estimator,
   query-reuse history buffer, convergence evaluation, or speedup comparison.

## Current evidence boundary

- Finite proxy diagnostics passed: 3/4.
- Negative finite diagnostics: 1.
- Scoped evidence points: 8/12.
- Complete paper claims independently verified: 0/6.
- Current external score claim: false.
- Author endorsement: not claimed.

Passing finite proxies mean only that the recorded toy computations behave as
described. They do not establish the paper's general propositions, stochastic
assumptions, query-reuse method, optimizer, or empirical results.

## What is not reproduced

- The official variance-reduced ZoVH implementation and history buffer.
- Inverse-Hessian and inverse-Hessian-gradient-product estimators.
- The curvature-aware ZOO optimizer and convergence curves.
- The complete Figure 2 protocol and equal-budget comparisons.
- The MNIST black-box attack.
- Synthetic speedup experiments and LLM fine-tuning.
- Formal proofs and paper-wide stochastic-noise assumptions.

## Repository map

- repro/src/core.py — finite Hessian forms, smoothed references, baseline
  diagnostics, and central differences.
- repro/src/verify.py — existing bounded C1–C4 diagnostics.
- repro/src/finalize_gate.py — canonical six-claim ledger and gate.
- outputs/diagnostics.json — existing raw measurements.
- outputs/verdict.json — canonical claim/evidence/status report.
- outputs/gate.json — scoped machine-readable gate.
- publication_gate.json — root-level publication metadata.
- CLAIM_EVIDENCE.md — claim-to-code-to-output production ledger.
- SOURCE_AUDIT.md — paper provenance and missing evidence.
- ENVIRONMENT.md — runtime assumptions and commands.
- REPORT.md — publication boundary and upgrade requirements.
- verify_final.py — fail-closed repository-state verifier.
- docs/paper.html and docs/paper.txt — cached paper reference material.

## Branches

The source repository exposed master and is normalized to one canonical main
branch. There are no experiment, orx/*, or paper-version branches in scope.
Branch cleanup is administrative and does not increase scientific evidence.

## Citation

~~~bibtex
@inproceedings{qiu2026zovh,
  title={Revisiting Zeroth-Order Hessian Approximation: A Single-Step Policy Optimization Lens},
  author={Qiu, Junbin and Hong, Zhaowei and Xu, Renzhe and Shu, Yao},
  booktitle={Proceedings of the 43rd International Conference on Machine Learning},
  year={2026},
  eprint={2605.30960},
  archivePrefix={arXiv},
  url={https://arxiv.org/abs/2605.30960}
}
~~~

Please cite the paper for its research claims and this repository for the
independent bounded audit artifacts.

## Thank you

Thank you to Junbin Qiu, Zhaowei Hong, Renzhe Xu, and Yao Shu for making the
paper, derivations, empirical protocol, and official code available. This
audit is intended as a transparent, limited reproduction record that makes
clear what was checked, what was not checked, and where the clean-room
implementation differs from the full ZoVH system.

This note is an expression of appreciation only; the authors did not review,
endorse, or maintain this independent repository.

## Attribution

Repository documentation and commits are attributed to
MachineLearning-Nerd using
MachineLearning-Nerd@users.noreply.github.com.
