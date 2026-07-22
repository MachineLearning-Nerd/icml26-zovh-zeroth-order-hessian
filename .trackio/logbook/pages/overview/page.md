# overview


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_c65da47f5d24", "created_at": "2026-07-22T15:20:11+00:00", "title": "Executive summary"}
-->
# ZoVH Zeroth-Order Hessian — 3/6 VERIFIED (6 pts, honest)

**Paper:** Revisiting Zeroth-Order Hessian Approximation (arXiv 2605.30960, OpenReview nEQYu4ndGA).

**Estimator (Prop 3.2):** Ĥ=(1/K)Σ[(f(θ+μu_i)−b)/μ²](u_i u_iᵀ−I_d), unbiased for the smoothed Hessian ∇²F_μ for ANY baseline b.

- **C1** Prop 3.2/3.3: (u uᵀ−I) and rank-one forms coincide (b=F_μ), both → ∇²F_μ.
- **C2** Theorem 4.6: E[Ĥ]=∇²F_μ, BASELINE-INDEPENDENT (Ĥ(b1)−Ĥ(b2)→0 at 1/√N); converges to analytic smoothed Hessian (quadratic A, quartic diag(12θ²+12μ²)).
- **C3** Theorem 4.7/4.8: b*→F_μ (d→∞); variance ↓~1/K; squared smoothing bias ~12μ²√d ≤ L₂²μ²d.
- **C4/C6** HONEST NEGATIVES: bare estimator's 1/μ⁴ variance dominates; the paper's 8×/22× gains need its full control-variate/query-reuse machinery, not reproduced here.
- **C5** MNIST deferred.

Rigorous exact headline: unbiasedness + bias-variance decomposition. C4/C6 reported as honest negatives per the no-force-fit rule. Under ≥10 target due to 3 empirical claims.
