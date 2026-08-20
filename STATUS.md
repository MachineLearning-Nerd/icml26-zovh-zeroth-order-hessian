# nEQYu4ndGA — ZoVH Zeroth-Order Hessian

Overall status:
INCONCLUSIVE_C1_ALGEBRAIC_FINITE_PROXY_C2_FINITE_ANALYTIC_PROXY_C3_FINITE_BIAS_VARIANCE_PROXY_C4_HONEST_NEGATIVE_C5_C6_NOT_REPRODUCED_NO_PAPER_CLAIMS_VERIFIED_NO_CURRENT_SCORE

| Claim | Status | Evidence |
| --- | --- | --- |
| C1 Propositions 3.2 and 3.3 | ALGEBRAIC_FINITE_PROXY | Form difference 8.746309929968238e-16 |
| C2 Theorem 4.6 | FINITE_ANALYTIC_PROXY | Final quadratic/quartic errors 0.0194 and 0.0225 |
| C3 Theorems 4.7 and 4.8 | FINITE_BIAS_VARIANCE_PROXY | MSE decreases from 603.182 to 53.729 with K |
| C4 Figure 2 | HONEST_NEGATIVE | Bare estimator error 75.504 versus central difference 0.0016 |
| C5 MNIST attack | NOT_REPRODUCED | Data and attack implementation absent |
| C6 synthetic speedup | NOT_REPRODUCED | Optimizer and speedup runs absent |

- Finite proxy diagnostics passed: 3/4.
- Negative finite diagnostics: 1.
- Scoped evidence points: 8/12.
- Complete paper claims independently verified: 0/6.
- Current external score claim: false.
- Canonical branch: main.
- Canonical attribution: MachineLearning-Nerd.

See CLAIM_EVIDENCE.md and outputs/verdict.json for the production ledger.
