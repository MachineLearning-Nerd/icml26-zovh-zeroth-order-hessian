# Independent audit report

## Executive result

The bounded audit is INCONCLUSIVE. Three of four finite diagnostics pass, one
finite diagnostic is an honest negative, and zero of six complete paper claims
are independently verified.

The repository is ready to publish as a clearly scoped evidence audit. It is
not ready to be described as a full reproduction and makes no current
external score claim.

## Results

| Area | Result | Interpretation |
| --- | --- | --- |
| Finite diagnostics | 3/4 | Existing bounded checks pass |
| C1 estimator forms | ALGEBRAIC_FINITE_PROXY | Finite quadratic identity check |
| C2 unbiasedness | FINITE_ANALYTIC_PROXY | Toy analytic convergence |
| C3 bias-variance | FINITE_BIAS_VARIANCE_PROXY | Finite trend checks |
| C4 Figure 2 | HONEST_NEGATIVE | Bare estimator loses to central differences |
| C5 MNIST attack | NOT_REPRODUCED | Data and attack absent |
| C6 synthetic speedup | NOT_REPRODUCED | Optimizer and runs absent |
| Complete paper claims | 0/6 | No paper-level claim is verified |
| Current external score | false | No score is asserted |

## Upgrade requirements

Reproduction would require the official variance-reduced implementation,
query-reuse protocol, complete optimizer, exact paper-scale comparisons, MNIST
attack, synthetic speedup, and comparable data and runtime outputs.

Until then, publication_gate.json allows sharing the bounded audit package
only; complete paper reproduction remains disallowed.
