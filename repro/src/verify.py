"""Run bounded finite diagnostics for arXiv 2605.30960 (ZoVH).

The diagnostics exercise four narrow pieces of the paper on deterministic
analytic toy objectives.  They are evidence for those finite proxies, not
proof of the paper's general theorems or reproduction of its experiments.

C1  Propositions 3.2/3.3: compare the two estimator forms on shared directions.
C2  Theorem 4.6: measure finite-sample baseline differences and convergence to
    analytic smoothed Hessians.
C3  Theorems 4.7/4.8: measure finite baseline concentration, K-dependent MSE,
    and smoothing-bias scaling with a loose toy bound.
C4  Figure 2 diagnostic: compare the bare single-batch estimator with central
    differences under one fixed synthetic setting; this is an honest negative.

C5 (MNIST attack) and C6 (synthetic optimization speedup) are not run here.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from core import (  # noqa: E402
    central_difference_hessian,
    make_quadratic,
    make_quartic,
    optimal_baseline,
    smoothed_hessian_mc,
    smoothed_value,
    zovh_estimator_prop32,
)

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
os.makedirs(OUT, exist_ok=True)


def _hessian_from_directions(f, theta, mu, baseline, directions):
    """Evaluate the Proposition 3.2 form on a shared finite direction sample."""
    directions = np.asarray(directions)
    n, d = directions.shape
    values = np.asarray([f(theta + mu * u) for u in directions])
    weighted = directions * (values - baseline)[:, None]
    hessian = directions.T @ weighted / (mu**2 * n)
    correction = np.eye(d) * np.mean(values - baseline) / mu**2
    return hessian - correction


def _rank_one_from_directions(f, theta, mu, baseline, directions):
    """Evaluate the Proposition 3.3 rank-one form on shared directions."""
    directions = np.asarray(directions)
    n, _ = directions.shape
    values = np.asarray([f(theta + mu * u) for u in directions])
    weighted = directions * (values - baseline)[:, None]
    return directions.T @ weighted / (mu**2 * n)


def claim_c1_proxy():
    rng = np.random.default_rng(1)
    d, mu, n = 4, 0.3, 200_000
    matrix = rng.normal(size=(d, d))
    matrix = matrix @ matrix.T / d
    objective, _ = make_quadratic(matrix, rng.normal(size=d))
    theta = rng.normal(size=d) * 0.5
    directions = rng.standard_normal(size=(n, d))
    values = np.asarray([objective(theta + mu * u) for u in directions])
    f_mu = float(np.mean(values))

    hessian_32 = _hessian_from_directions(
        objective, theta, mu, f_mu, directions
    )
    hessian_rank_one = _rank_one_from_directions(
        objective, theta, mu, f_mu, directions
    )
    form_difference = float(np.linalg.norm(hessian_32 - hessian_rank_one))
    prop32_error = float(np.linalg.norm(hessian_32 - matrix))
    rank_one_error = float(np.linalg.norm(hessian_rank_one - matrix))
    passed = bool(
        form_difference < 1e-9
        and prop32_error < 0.1
        and rank_one_error < 0.1
    )

    return {
        "paper_claim": "Propositions 3.2 and 3.3",
        "diagnostic": "shared finite Gaussian directions on a quadratic",
        "prop32_to_quadratic_hessian_error": prop32_error,
        "rank_one_to_quadratic_hessian_error": rank_one_error,
        "form_difference": form_difference,
        "finite_proxy_passed": passed,
        "status": "ALGEBRAIC_FINITE_PROXY",
        "limitation": (
            "A finite sample check of the two formulas; it is not a proof of "
            "the propositions for arbitrary stochastic objectives."
        ),
    }


def claim_c2_proxy():
    rng = np.random.default_rng(3)
    d, mu = 5, 0.3
    matrix = rng.normal(size=(d, d))
    matrix = matrix @ matrix.T / d
    objective, _ = make_quadratic(matrix, rng.normal(size=d))
    theta = rng.normal(size=d) * 0.5
    f_mu = smoothed_value(
        objective, theta, mu, np.random.default_rng(4), N=20_000
    )

    sample_sizes = [2_000, 8_000, 32_000, 128_000]
    baseline_differences = []
    gram_errors = []
    for n in sample_sizes:
        directions = rng.standard_normal(size=(n, d))
        hessian_zero = _hessian_from_directions(
            objective, theta, mu, 0.0, directions
        )
        hessian_f_mu = _hessian_from_directions(
            objective, theta, mu, f_mu, directions
        )
        baseline_differences.append(
            float(np.linalg.norm(hessian_zero - hessian_f_mu))
        )
        gram_errors.append(
            float(np.linalg.norm(directions.T @ directions / n - np.eye(d)))
        )

    quadratic_sizes = [5_000, 20_000, 80_000, 320_000]
    quadratic_errors = []
    for n in quadratic_sizes:
        directions = rng.standard_normal(size=(n, d))
        estimate = _hessian_from_directions(
            objective, theta, mu, f_mu, directions
        )
        quadratic_errors.append(
            float(np.linalg.norm(estimate - matrix) / np.linalg.norm(matrix))
        )

    quartic, _ = make_quartic()
    quartic_hessian = np.diag(12 * theta**2 + 12 * mu**2)
    quartic_f_mu = smoothed_value(
        quartic, theta, mu, np.random.default_rng(5), N=20_000
    )
    quartic_errors = []
    for n in quadratic_sizes:
        directions = rng.standard_normal(size=(n, d))
        estimate = _hessian_from_directions(
            quartic, theta, mu, quartic_f_mu, directions
        )
        quartic_errors.append(
            float(
                np.linalg.norm(estimate - quartic_hessian)
                / np.linalg.norm(quartic_hessian)
            )
        )

    baseline_shrinks = baseline_differences[-1] < baseline_differences[0] * 0.2
    convergence_improves = bool(
        quadratic_errors[-1] < quadratic_errors[0] * 0.4
        and quartic_errors[-1] < quartic_errors[0] * 0.6
    )
    passed = bool(
        baseline_shrinks
        and convergence_improves
        and quadratic_errors[-1] < 0.10
        and quartic_errors[-1] < 0.12
    )

    return {
        "paper_claim": "Theorem 4.6",
        "diagnostic": (
            "finite baseline-difference scaling plus analytic quadratic and "
            "quartic smoothed-Hessian convergence"
        ),
        "baseline_diff_by_sample_size": {
            str(n): round(value, 4)
            for n, value in zip(sample_sizes, baseline_differences)
        },
        "gram_error_by_sample_size": {
            str(n): round(value, 4)
            for n, value in zip(sample_sizes, gram_errors)
        },
        "quadratic_relative_error_by_sample_size": {
            str(n): round(value, 4)
            for n, value in zip(quadratic_sizes, quadratic_errors)
        },
        "quartic_relative_error_by_sample_size": {
            str(n): round(value, 4)
            for n, value in zip(quadratic_sizes, quartic_errors)
        },
        "baseline_difference_shrinks": bool(baseline_shrinks),
        "analytic_convergence_improves": convergence_improves,
        "finite_proxy_passed": passed,
        "status": "FINITE_ANALYTIC_PROXY",
        "limitation": (
            "Finite Monte Carlo behavior on two noiseless toy objectives; it "
            "does not establish the theorem under the paper's stochastic "
            "assumptions."
        ),
    }


def claim_c3_proxy():
    rng = np.random.default_rng(6)
    baseline_records = []
    for dimension in [3, 6, 12, 24]:
        mu = 0.2
        quartic, _ = make_quartic()
        theta = rng.normal(size=dimension) * 0.3
        f_mu = smoothed_value(
            quartic, theta, mu, np.random.default_rng(7), N=6_000
        )
        baseline = optimal_baseline(
            quartic, theta, mu, np.random.default_rng(8), N=6_000
        )
        baseline_records.append(
            {
                "dimension": dimension,
                "relative_difference": round(
                    abs(baseline - f_mu) / abs(f_mu), 4
                ),
            }
        )
    relative_differences = [
        record["relative_difference"] for record in baseline_records
    ]

    dimension, mu = 6, 0.15
    matrix = rng.normal(size=(dimension, dimension))
    matrix = matrix @ matrix.T / dimension
    quadratic, _ = make_quadratic(matrix, rng.normal(size=dimension))
    theta = rng.normal(size=dimension) * 0.4
    f_mu = smoothed_value(
        quadratic, theta, mu, np.random.default_rng(9), N=8_000
    )
    ks = [20, 50, 100, 200]
    mse_by_k = []
    for k in ks:
        errors = [
            float(
                np.linalg.norm(
                    zovh_estimator_prop32(
                        quadratic,
                        theta,
                        mu,
                        k,
                        f_mu,
                        np.random.default_rng(100 + seed),
                    )
                    - matrix
                )
                ** 2
            )
            for seed in range(60)
        ]
        mse_by_k.append(float(np.mean(errors)))

    quartic, quartic_hessian = make_quartic()
    theta = rng.normal(size=dimension) * 0.4
    unsmoothed_hessian = quartic_hessian(theta)
    lipschitz_proxy = 24.0 * np.max(np.abs(theta))
    mus = [0.05, 0.1, 0.2, 0.4]
    squared_bias = []
    bounds = []
    for smoothing in mus:
        smoothed_hessian = smoothed_hessian_mc(
            quartic_hessian,
            theta,
            smoothing,
            np.random.default_rng(11),
            N=8_000,
        )
        squared_bias.append(
            float(np.linalg.norm(smoothed_hessian - unsmoothed_hessian) ** 2)
        )
        bounds.append(
            float(lipschitz_proxy**2 * smoothing**2 * dimension)
        )

    baseline_concentration = relative_differences[-1] < relative_differences[0]
    variance_decreases = mse_by_k[-1] < mse_by_k[0] * 0.4
    bias_increases = squared_bias[-1] > squared_bias[0] * 2
    bias_below_bound = all(
        squared_bias[index] <= bounds[index] * 1.5
        for index in range(len(mus))
    )
    passed = bool(
        baseline_concentration
        and variance_decreases
        and bias_increases
        and bias_below_bound
    )

    return {
        "paper_claim": "Theorems 4.7 and 4.8",
        "diagnostic": (
            "finite baseline concentration, K-dependent MSE, and quartic "
            "smoothing-bias scaling"
        ),
        "baseline_concentration": baseline_records,
        "mse_by_K": {
            str(k): round(value, 3) for k, value in zip(ks, mse_by_k)
        },
        "squared_bias_by_mu": {
            str(smoothing): round(value, 3)
            for smoothing, value in zip(mus, squared_bias)
        },
        "loose_toy_bound_by_mu": {
            str(smoothing): round(value, 3)
            for smoothing, value in zip(mus, bounds)
        },
        "baseline_concentration_improves": bool(baseline_concentration),
        "mse_decreases_with_K": bool(variance_decreases),
        "smoothing_bias_increases": bool(bias_increases),
        "squared_bias_below_loose_bound": bool(bias_below_bound),
        "finite_proxy_passed": passed,
        "status": "FINITE_BIAS_VARIANCE_PROXY",
        "limitation": (
            "A finite toy trend check with a loose local bound; it does not "
            "verify the theorem's constants, assumptions, query reuse, or "
            "stochastic-noise model."
        ),
    }


def claim_c4_negative():
    rng = np.random.default_rng(13)
    dimension = 6

    def styblinski_tang(theta):
        return float(np.sum(theta**4 - 16 * theta**2 + 5 * theta) / 2)

    theta = np.ones(dimension) * 0.5
    reference = central_difference_hessian(styblinski_tang, theta, h=1e-6)
    mu = 0.1
    f_mu = smoothed_value(
        styblinski_tang, theta, mu, np.random.default_rng(14), N=8_000
    )
    bare_errors = [
        float(
            np.linalg.norm(
                zovh_estimator_prop32(
                    styblinski_tang,
                    theta,
                    mu,
                    200,
                    f_mu,
                    np.random.default_rng(200 + seed),
                )
                - reference
            )
        )
        for seed in range(40)
    ]
    central_difference_error = float(
        np.linalg.norm(
            central_difference_hessian(styblinski_tang, theta, h=1e-4)
            - reference
        )
    )
    bare_error = float(np.mean(bare_errors))
    passed = bool(bare_error < central_difference_error)

    return {
        "paper_claim": "Figure 2 accuracy comparison",
        "diagnostic": (
            "bare Proposition 3.2 estimator versus central differences on "
            "Styblinski-Tang at one fixed setting"
        ),
        "bare_zovh_error_K200": round(bare_error, 3),
        "central_difference_error": round(central_difference_error, 4),
        "bare_zovh_beats_central_difference": passed,
        "finite_proxy_passed": False,
        "status": "HONEST_NEGATIVE",
        "limitation": (
            "This is not the paper's Figure 2 protocol or an equal-budget "
            "reproduction: query reuse, control variates, competing "
            "estimators, and all reported settings are absent."
        ),
    }


def main():
    claims = {
        "C1_estimator_forms_proxy": claim_c1_proxy(),
        "C2_unbiasedness_proxy": claim_c2_proxy(),
        "C3_bias_variance_proxy": claim_c3_proxy(),
        "C4_central_difference_proxy": claim_c4_negative(),
    }
    finite_passed = sum(
        claim["finite_proxy_passed"] for claim in claims.values()
    )
    diagnostics = {
        "paper": "Revisiting Zeroth-Order Hessian Approximation: A Single-Step Policy Optimization Lens",
        "authors": ["Junbin Qiu", "Zhaowei Hong", "Renzhe Xu", "Yao Shu"],
        "arxiv": "2605.30960",
        "openreview": "nEQYu4ndGA",
        "scope": "bounded_clean_room_single_batch_analytic_toy_proxy",
        "claims": claims,
        "finite_proxy_diagnostics_passed": finite_passed,
        "finite_proxy_diagnostics_total": len(claims),
        "negative_diagnostics": 1,
        "paper_claims_verified": 0,
        "paper_claims_total": 6,
        "not_run": [
            "C5: MNIST black-box adversarial attack",
            "C6: Section 6.2 synthetic optimization speedup",
        ],
        "overall_status": "INCONCLUSIVE",
    }
    for filename in ["diagnostics.json", "verdict.json"]:
        with open(os.path.join(OUT, filename), "w", encoding="utf-8") as handle:
            json.dump(diagnostics, handle, indent=2)
            handle.write("\n")

    for claim_id, claim in claims.items():
        print(
            f"{claim_id}: {claim['status']} "
            f"(finite proxy passed={claim['finite_proxy_passed']})"
        )
    print(
        f"\nFinite proxy diagnostics passed: {finite_passed}/{len(claims)}"
    )
    print("Paper-level claims independently verified: 0/6")
    print("Overall status: INCONCLUSIVE")
    print("Saved outputs/diagnostics.json and outputs/verdict.json")


if __name__ == "__main__":
    main()
