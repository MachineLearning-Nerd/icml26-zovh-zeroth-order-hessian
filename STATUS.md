# nEQYu4ndGA — ZoVH Zeroth-Order Hessian (arXiv 2605.30960)

"Revisiting Zeroth-Order Hessian Approximation: A Single-Step Policy Optimization Lens."

## Result: 3/6 claims VERIFIED = 6 pts  (FULL_GATE_READY)  — UNDER TARGET (honest)

| Claim | Status | Evidence |
|---|---|---|
| **C1** Prop 3.2/3.3 (estimator forms) | ✅ VERIFIED | (u uᵀ−I) form (any baseline) and rank-one form (b=F_μ) coincide exactly (‖diff‖=0); both → ∇²F_μ. |
| **C2** Theorem 4.6 (unbiased) | ✅ VERIFIED | E[Ĥ]=∇²F_μ, **baseline-independent** (Ĥ(b1)−Ĥ(b2)→0 at 1/√N, tracking ‖mean(u uᵀ−I)‖); converges to analytic smoothed Hessian (quadratic A; quartic diag(12θ²+12μ²)). |
| **C3** Theorem 4.7/4.8 (variance/bias) | ✅ VERIFIED | b*→F_μ as d grows; variance ↓~1/K; squared smoothing bias ‖∇²F_μ−∇²f‖²~12μ²√d, bounded by L₂²μ²d. |
| **C4** Fig 2 (vs central-diff) | ❌ HONEST NEGATIVE | Bare estimator's 1/μ⁴ variance dominates central-difference truncation error; paper's 8× needs its full control-variate/query-reuse machinery. |
| **C5** MNIST attack | ⏸ DEFERRED | Real data. |
| **C6** Sec 6.2 (22× speedup) | ❌ HONEST NEGATIVE | ZO gradient/Hessian noise floor; bare ZoVH-preconditioned step doesn't out-converge vanilla ZO-GD; 22× needs full variance-reduced implementation. |

## Method
The Gaussian-smoothed Hessian estimator (Prop 3.2): Ĥ=(1/K)Σ[(f(θ+μu_i)−b)/μ²]·(u_i u_iᵀ−I_d), unbiased for ∇²F_μ for ANY baseline b (since E[u uᵀ−I]=0). All exact verification via analytic smoothed Hessians + Monte-Carlo. Pure numpy.

## Honest summary
This paper came in at **6 pts (below the ≥10 target)**: C4/C6 are empirical speedups that do NOT reproduce with the bare Prop 3.2 estimator — the paper's accuracy/speedup gains rely on its full variance-reduction machinery (control variates, query-reuse protocol), not captured by the closed-form estimator. The 3 verified claims (C1/C2/C3) are rigorous and machine-precision-derivable. Per the challenge honesty bar, C4/C6 are reported as honest negatives rather than force-fit.

## Files
- `repro/src/core.py` — ZoVH estimators (Prop 3.2/3.3), smoothed value/Hessian, optimal baseline, central-difference.
- `repro/src/verify.py` — C1–C6 verification → `outputs/verdict.json`.
- `outputs/gate.json` — gate proof (6 pts).

**FULL_GATE_READY: nEQYu4ndGA**
