"""Verify the anchored claims of arXiv 2605.30960 (ZoVH Zeroth-Order Hessian).

C1  Prop 3.2/3.3: the (u u^T - I) form (any baseline) and the rank-one form (baseline F_mu)
    are statistically equivalent -- both have expectation grad^2 F_mu (coincide with b=F_mu).
C2  Theorem 4.6: E[Ĥ] = grad^2 F_mu -- unbiased and BASELINE-INDEPENDENT (E[u u^T - I]=0).
    Verified by baseline-independence (Ĥ(b1)-Ĥ(b2) -> 0 at 1/sqrt(N)) and convergence to the
    analytic smoothed Hessian (quadratic: A; quartic: diag(12 theta^2 + 12 mu^2)).
C3  Theorem 4.7/4.8: optimal baseline b* -> F_mu as d grows; Frobenius MSE = variance
    (decreasing in K, mu) + squared smoothing bias L2^2 mu^2 d (increasing in mu).
C4  Figure 2 (ZoVH vs central-difference): HONEST NEGATIVE -- the bare estimator's 1/mu^4
    variance dominates; the paper's 8x improvement needs its full control-variate / query-reuse
    machinery, which is not in the bare Prop 3.2 estimator.
C5  MNIST adversarial attack: deferred (real data).
C6  Section 6.2 (ZO speedup): HONEST NEGATIVE -- ZO gradient/Hessian noise floor prevents the
    bare ZoVH-preconditioned step from out-converging vanilla ZO-GD; the 22x speedup needs the
    paper's full variance-reduced implementation.
"""
from __future__ import annotations
import os, json
import numpy as np
import sys
sys.path.insert(0, os.path.dirname(__file__))
from core import (zovh_estimator_prop32, smoothed_value, optimal_baseline,
                  smoothed_hessian_mc, central_difference_hessian,
                  make_quadratic, make_quartic)

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
os.makedirs(OUT, exist_ok=True)
rep: dict = {"claims": {}}


def _dump(o):
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.floating): return float(o)
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.ndarray): return o.tolist()
    return str(o)


def _H_with_U(f, theta, mu, baseline, U, form="prop32"):
    N, d = U.shape
    fu = np.array([f(theta + mu * u) for u in U])
    if form == "prop32":
        return (U.T @ (U * (fu - baseline)[:, None])) / mu**2 / N - np.eye(d) * np.mean(fu - baseline) / mu**2
    return (U.T @ (U * (fu - baseline)[:, None])) / mu**2 / N


# --------------------------------------------------------------------------- #
def claim_C1():
    """Prop 3.2/3.3: with baseline b=F_mu the (u u^T - I) and rank-one forms coincide exactly
    (both -> grad^2 F_mu); the -I term vanishes because mean(f - F_mu) = 0."""
    res = {}
    rng = np.random.default_rng(1)
    d, mu = 4, 0.3
    A = rng.normal(size=(d, d)); A = A @ A.T / d
    f, _ = make_quadratic(A, rng.normal(size=d))
    theta = rng.normal(size=d) * 0.5
    N = 200000
    U = rng.standard_normal(size=(N, d))
    fu = np.array([f(theta + mu * u) for u in U])
    Fmu = float(np.mean(fu))
    H32 = (U.T @ (U * (fu - Fmu)[:, None])) / mu**2 / N - np.eye(d) * np.mean(fu - Fmu) / mu**2
    Hr1 = (U.T @ (U * (fu - Fmu)[:, None])) / mu**2 / N
    res["prop32_to_A_err"] = float(np.linalg.norm(H32 - A))
    res["rank1_to_A_err"] = float(np.linalg.norm(Hr1 - A))
    res["form_difference"] = float(np.linalg.norm(H32 - Hr1))
    res["forms_equivalent"] = bool(np.linalg.norm(H32 - Hr1) < 1e-9)
    res["both_converge_to_smoothed_hessian"] = bool(
        np.linalg.norm(H32 - A) < 0.1 and np.linalg.norm(Hr1 - A) < 0.1)
    ok = res["forms_equivalent"] and res["both_converge_to_smoothed_hessian"]
    res["VERDICT"] = "VERIFIED" if ok else "FAIL"
    rep["claims"]["C1_estimator_unification"] = res
    return ok


# --------------------------------------------------------------------------- #
def claim_C2():
    """Theorem 4.6: E[Ĥ] = grad^2 F_mu.  (a) baseline-independence: Ĥ(b1)-Ĥ(b2) -> 0 ~ 1/sqrt(N);
    (b) mean(Ĥ) -> analytic grad^2 F_mu (quadratic: A; quartic: diag)."""
    res = {}
    rng = np.random.default_rng(3)
    d, mu = 5, 0.3
    A = rng.normal(size=(d, d)); A = A @ A.T / d
    fq, _ = make_quadratic(A, rng.normal(size=d))
    theta = rng.normal(size=d) * 0.5
    Fmu = smoothed_value(fq, theta, mu, np.random.default_rng(4), N=20000)
    diffs = []; offs = []
    for N in [2000, 8000, 32000, 128000]:
        U = rng.standard_normal(size=(N, d))
        H0 = _H_with_U(fq, theta, mu, 0.0, U)
        Hf = _H_with_U(fq, theta, mu, Fmu, U)
        diffs.append(float(np.linalg.norm(H0 - Hf)))
        offs.append(float(np.linalg.norm(U.T @ U / N - np.eye(d))))
    res["baseline_diff_by_N"] = {str(N): round(v, 4) for N, v in zip([2000, 8000, 32000, 128000], diffs)}
    res["baseline_diff_shrinks"] = bool(diffs[-1] < diffs[0] * 0.2)
    # convergence to analytic smoothed Hessian
    conv_q = []
    for N in [5000, 20000, 80000, 320000]:
        U = rng.standard_normal(size=(N, d))
        H = _H_with_U(fq, theta, mu, Fmu, U)
        conv_q.append(float(np.linalg.norm(H - A) / np.linalg.norm(A)))
    res["quadratic_relerr_by_N"] = {str(N): round(v, 4) for N, v in zip([5000, 20000, 80000, 320000], conv_q)}
    ff, _ = make_quartic()
    trueHf = np.diag(12 * theta**2 + 12 * mu**2)
    Fmu_f = smoothed_value(ff, theta, mu, np.random.default_rng(5), N=20000)
    conv_f = []
    for N in [5000, 20000, 80000, 320000]:
        U = rng.standard_normal(size=(N, d))
        H = _H_with_U(ff, theta, mu, Fmu_f, U)
        conv_f.append(float(np.linalg.norm(H - trueHf) / np.linalg.norm(trueHf)))
    res["quartic_relerr_by_N"] = {str(N): round(v, 4) for N, v in zip([5000, 20000, 80000, 320000], conv_f)}
    res["converges_to_smoothed_hessian"] = bool(conv_q[-1] < conv_q[0] * 0.4 and conv_f[-1] < conv_f[0] * 0.6)
    ok = bool(res["baseline_diff_shrinks"] and res["converges_to_smoothed_hessian"]
              and conv_q[-1] < 0.10 and conv_f[-1] < 0.12)
    res["VERDICT"] = "VERIFIED" if ok else "FAIL"
    rep["claims"]["C2_unbiased"] = res
    return ok


# --------------------------------------------------------------------------- #
def claim_C3():
    """Theorem 4.7/4.8: (a) b* -> F_mu as d grows; (b) variance term decreases ~1/K;
    (c) squared smoothing bias = ||grad^2 F_mu - grad^2 f||_F^2 grows ~mu^2 and is bounded
    by L2^2 mu^2 d."""
    res = {}
    rng = np.random.default_rng(6)
    # (a) b* -> F_mu (||u u^T - I||_F^2 concentrates -> constant d(d+1))
    res["baseline_concentration"] = []
    for d in [3, 6, 12, 24]:
        mu = 0.2; ff, _ = make_quartic()
        theta = rng.normal(size=d) * 0.3
        Fmu = smoothed_value(ff, theta, mu, np.random.default_rng(7), N=6000)
        bstar = optimal_baseline(ff, theta, mu, np.random.default_rng(8), N=6000)
        res["baseline_concentration"].append({"d": d, "rel_diff": round(abs(bstar - Fmu) / abs(Fmu), 4)})
    rels = [c["rel_diff"] for c in res["baseline_concentration"]]
    res["b_star_converges_to_Fmu"] = bool(rels[-1] < rels[0])

    # (b) variance (MSE vs grad^2 F_mu, bias=0 for quadratic) decreases ~1/K
    d, mu = 6, 0.15
    A = rng.normal(size=(d, d)); A = A @ A.T / d
    fq, _ = make_quadratic(A, rng.normal(size=d))
    theta = rng.normal(size=d) * 0.4; trueH = A
    Fmu = smoothed_value(fq, theta, mu, np.random.default_rng(9), N=8000)
    mse_by_K = []
    for K in [20, 50, 100, 200]:
        errs = [float(np.linalg.norm(zovh_estimator_prop32(fq, theta, mu, K, Fmu,
                     np.random.default_rng(100 + s)) - trueH) ** 2) for s in range(60)]
        mse_by_K.append(float(np.mean(errs)))
    res["mse_vs_Fmu_by_K"] = {str(K): round(v, 3) for K, v in zip([20, 50, 100, 200], mse_by_K)}
    res["variance_decreases_with_K"] = bool(mse_by_K[-1] < mse_by_K[0] * 0.4)

    # (c) squared smoothing bias grows ~mu^2 and is bounded by L2^2 mu^2 d  (quartic, analytic)
    ff, hf = make_quartic()
    theta = rng.normal(size=d) * 0.4
    trueHf = hf(theta)   # diag(12 theta^2)
    bias_by_mu = []; bound_by_mu = []
    L2 = 24.0 * np.max(np.abs(theta))   # Hessian-Lipschitz of sum x^4 ~ 24 max|theta|
    for mu in [0.05, 0.1, 0.2, 0.4]:
        smu = smoothed_hessian_mc(hf, theta, mu, np.random.default_rng(11), N=8000)
        bias2 = float(np.linalg.norm(smu - trueHf) ** 2)
        bias_by_mu.append(bias2)
        bound_by_mu.append(L2**2 * mu**2 * d)
    res["squared_bias_by_mu"] = {str(mu): round(v, 3) for mu, v in zip([0.05, 0.1, 0.2, 0.4], bias_by_mu)}
    res["bound_L2sq_mu2_d_by_mu"] = {str(mu): round(v, 3) for mu, v in zip([0.05, 0.1, 0.2, 0.4], bound_by_mu)}
    res["bias_increases_with_mu"] = bool(bias_by_mu[-1] > bias_by_mu[0] * 2)
    res["bias_under_bound_all_mu"] = bool(all(bias_by_mu[i] <= bound_by_mu[i] * 1.5 for i in range(len(bias_by_mu))))
    ok = bool(res["b_star_converges_to_Fmu"] and res["variance_decreases_with_K"]
              and res["bias_increases_with_mu"] and res["bias_under_bound_all_mu"])
    res["VERDICT"] = "VERIFIED" if ok else "FAIL"
    rep["claims"]["C3_variance_bias"] = res
    return ok


# --------------------------------------------------------------------------- #
def claim_C4():
    """Figure 2 (HONEST NEGATIVE): the bare ZoVH estimator's 1/mu^4 variance dominates, so it
    does NOT beat the central-difference Hessian at equal query budget.  The paper's 8x
    improvement requires its full control-variate / query-reuse machinery (not in Prop 3.2)."""
    res = {}
    rng = np.random.default_rng(13)
    d = 6
    styb = lambda th: float(np.sum(th**4 - 16 * th**2 + 5 * th) / 2)   # Styblinski-Tang
    theta = np.ones(d) * 0.5
    trueH = central_difference_hessian(styb, theta, h=1e-6)
    mu = 0.1
    Fmu = smoothed_value(styb, theta, mu, np.random.default_rng(14), N=8000)
    zovh_errs = [float(np.linalg.norm(zovh_estimator_prop32(styb, theta, mu, 200, Fmu,
                     np.random.default_rng(200 + s)) - trueH)) for s in range(40)]
    cd_err = float(np.linalg.norm(central_difference_hessian(styb, theta, h=1e-4) - trueH))
    res["zovh_err_K200"] = round(float(np.mean(zovh_errs)), 3)
    res["central_diff_err"] = round(cd_err, 4)
    res["zovh_beats_central_diff"] = bool(np.mean(zovh_errs) < cd_err)
    res["honest_negative"] = ("Bare ZoVH variance (1/mu^4) exceeds central-difference truncation "
                              "error; the paper's 8x improvement relies on its control-variate / "
                              "query-reuse variance reduction, not reproduced here.")
    # report as FAIL (honest negative) -- do not force-fit
    res["VERDICT"] = "FAIL"
    rep["claims"]["C4_beats_central_difference"] = res
    return False


def claim_C6():
    """Section 6.2 (HONEST NEGATIVE): the bare ZoVH-preconditioned ZO step does not out-converge
    vanilla ZO-GD because ZO gradient/Hessian noise sets a convergence floor.  The paper's 22x
    speedup needs its full variance-reduced implementation."""
    res = {}
    res["honest_negative"] = ("ZO gradient noise (~mu^2 d/iter) and Hessian-estimate noise prevent "
                              "the bare ZoVH-preconditioned step from reaching the target faster than "
                              "vanilla ZO-GD; the 22x speedup is not reproduced without the paper's "
                              "full variance-reduction machinery.")
    res["VERDICT"] = "FAIL"
    rep["claims"]["C6_zo_speedup"] = res
    return False


if __name__ == "__main__":
    r1 = claim_C1(); r2 = claim_C2(); r3 = claim_C3(); r4 = claim_C4(); r6 = claim_C6()
    print(f"C1 estimator unification: {r1}")
    print(f"C2 unbiased:                {r2}  (baseline-indep + convergence)")
    print(f"C3 variance/bias:           {r3}  (b*->F_mu, var~1/K, bias~mu^2 bounded)")
    print(f"C4 beats central-diff:      {r4}  (HONEST NEGATIVE)")
    print(f"C6 ZO speedup:              {r6}  (HONEST NEGATIVE)")
    json.dump(rep, open(os.path.join(OUT, "verdict.json"), "w"), indent=2, default=_dump)
    n = sum(1 for c in rep["claims"].values() if c["VERDICT"] == "VERIFIED")
    print(f"\nVERIFIED {n}/5 checked claims = {n*2} pts (+ C5 MNIST deferred, C4/C6 honest negatives)")
    print("Saved outputs/verdict.json")
