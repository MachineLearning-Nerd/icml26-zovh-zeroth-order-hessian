# overview

## ZoVH Zeroth-Order Hessian — bounded evidence audit

**Paper:** [Revisiting Zeroth-Order Hessian Approximation: A Single-Step Policy Optimization Lens](https://arxiv.org/abs/2605.30960)
**OpenReview:** nEQYu4ndGA
**Authors:** Junbin Qiu, Zhaowei Hong, Renzhe Xu, Yao Shu

**Overall status:** INCONCLUSIVE — 0/6 paper-level claims independently verified.

Three of four finite toy diagnostics pass. One fixed-setting bare-estimator comparison is negative. The MNIST attack and synthetic optimization speedup are not run.

| ID | Finite evidence | Status |
|---|---|---|
| C1 | Shared-direction comparison of Propositions 3.2 and 3.3 on a quadratic | ALGEBRAIC_FINITE_PROXY |
| C2 | Baseline-difference scaling and analytic quadratic/quartic convergence | FINITE_ANALYTIC_PROXY |
| C3 | Baseline concentration, MSE versus K, and quartic smoothing-bias trend | FINITE_BIAS_VARIANCE_PROXY |
| C4 | Bare Proposition 3.2 versus central difference on Styblinski-Tang | HONEST_NEGATIVE |
| C5 | MNIST black-box attack | NOT_REPRODUCED |
| C6 | Synthetic curvature-aware ZOO speedup | NOT_REPRODUCED |

The clean-room code does not include the official query-reuse history buffer, inverse-Hessian/product estimators, full optimizer, or paper datasets.
