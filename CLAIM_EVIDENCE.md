# Claim-to-evidence production ledger

This ledger maps the paper targets to the existing finite code and output
files. A finite proxy or negative is not a paper-level verification.

## Evidence accounting

| Claim | Scoped points | Available points | Status |
| --- | ---: | ---: | --- |
| C1 | 2 | 2 | ALGEBRAIC_FINITE_PROXY |
| C2 | 2 | 2 | FINITE_ANALYTIC_PROXY |
| C3 | 2 | 2 | FINITE_BIAS_VARIANCE_PROXY |
| C4 | 2 | 2 | HONEST_NEGATIVE |
| C5 | 0 | 2 | NOT_REPRODUCED |
| C6 | 0 | 2 | NOT_REPRODUCED |
| Total | 8 | 12 | INCONCLUSIVE |

The point count is an internal completeness accounting for this audit. It is
not a probability that a paper claim is true.

## C1 — estimator forms

- Paper target: Propositions 3.2 and 3.3.
- Production code: repro/src/core.py.
- Diagnostic runner: repro/src/verify.py, C1_estimator_forms_proxy.
- Raw output: outputs/diagnostics.json:C1_estimator_forms_proxy.
- Canonical ledger: repro/src/finalize_gate.py and outputs/verdict.json:C1.
- Finite result: shared Gaussian directions on a deterministic quadratic give
  form difference 8.746309929968238e-16; both Hessian errors are
  0.037952753942454544.
- Status: ALGEBRAIC_FINITE_PROXY.
- Limitation: this finite sample check is not a proof for arbitrary stochastic
  objectives.

## C2 — smoothed-Hessian unbiasedness

- Paper target: Theorem 4.6.
- Production code: repro/src/core.py.
- Diagnostic runner: repro/src/verify.py, C2_unbiasedness_proxy.
- Raw output: outputs/diagnostics.json:C2_unbiasedness_proxy.
- Canonical ledger: repro/src/finalize_gate.py and outputs/verdict.json:C2.
- Finite result: baseline differences shrink with shared sample size; final
  quadratic and quartic relative errors are 0.0194 and 0.0225.
- Status: FINITE_ANALYTIC_PROXY.
- Limitation: no stochastic function noise or theorem-level assumptions are
  exercised.

## C3 — baseline and bias-variance behavior

- Paper target: Theorems 4.7 and 4.8.
- Production code: repro/src/core.py.
- Diagnostic runner: repro/src/verify.py, C3_bias_variance_proxy.
- Raw output: outputs/diagnostics.json:C3_bias_variance_proxy.
- Canonical ledger: repro/src/finalize_gate.py and outputs/verdict.json:C3.
- Finite result: MSE decreases from 603.182 to 53.729 as K grows from 20 to
  200, while quartic smoothing bias increases with mu.
- Status: FINITE_BIAS_VARIANCE_PROXY.
- Limitation: finite toy trends do not verify constants, assumptions, query
  reuse, or the stochastic-noise model.

## C4 — accuracy comparison

- Paper target: Figure 2.
- Production code: repro/src/core.py.
- Diagnostic runner: repro/src/verify.py, C4_central_difference_proxy.
- Raw output: outputs/diagnostics.json:C4_central_difference_proxy.
- Canonical ledger: repro/src/finalize_gate.py and outputs/verdict.json:C4.
- Finite result: at K=200 and mu=0.1, bare estimator error is 75.504 while
  central-difference error is 0.0016.
- Status: HONEST_NEGATIVE.
- Limitation: this is not the complete Figure 2 protocol; query reuse,
  control variates, competing estimators, and all settings are absent.

## C5 — MNIST black-box attack

- Paper target: Section 6.3.
- Production path: README.md, STATUS.md, SOURCE_AUDIT.md, and outputs/verdict.json:C5.
- Status: NOT_REPRODUCED.
- Evidence produced: none. MNIST data, attack code, and reported runs are
  absent.

## C6 — synthetic curvature-aware speedup

- Paper target: Section 6.2.
- Production path: README.md, STATUS.md, SOURCE_AUDIT.md, and outputs/verdict.json:C6.
- Status: NOT_REPRODUCED.
- Evidence produced: none. The complete optimizer, inverse-Hessian/product
  estimators, query reuse, convergence curves, and speedup runs are absent.

## Reproduction boundary

The existing finite diagnostics are evidence about this bounded toy code only.
They do not reproduce the official ZoVH system or paper-wide experiments.
paper_claim_reproduced is explicitly false for every claim in claims.json.
