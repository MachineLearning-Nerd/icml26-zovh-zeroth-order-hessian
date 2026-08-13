"""Build the publication gate from the bounded ZoVH diagnostics."""
from __future__ import annotations

import json
import os


ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
OUTPUTS = os.path.join(ROOT, "outputs")


def main():
    with open(os.path.join(OUTPUTS, "diagnostics.json"), encoding="utf-8") as handle:
        diagnostics = json.load(handle)

    raw_claims = diagnostics["claims"]
    expected = {
        "C1_estimator_forms_proxy": "ALGEBRAIC_FINITE_PROXY",
        "C2_unbiasedness_proxy": "FINITE_ANALYTIC_PROXY",
        "C3_bias_variance_proxy": "FINITE_BIAS_VARIANCE_PROXY",
        "C4_central_difference_proxy": "HONEST_NEGATIVE",
    }
    raw_checks = all(
        key in raw_claims
        and raw_claims[key]["status"] == status
        for key, status in expected.items()
    )
    finite_passed = diagnostics["finite_proxy_diagnostics_passed"]
    finite_total = diagnostics["finite_proxy_diagnostics_total"]
    tests_passed = bool(
        raw_checks
        and finite_passed == 3
        and finite_total == 4
        and diagnostics["paper_claims_verified"] == 0
    )

    claims = [
        {
            "id": "C1",
            "paper_claim": "Propositions 3.2 and 3.3: Gaussian smoothed Hessian forms",
            "status": "ALGEBRAIC_FINITE_PROXY",
            "raw_diagnostic": "C1_estimator_forms_proxy",
            "evidence": (
                "Shared finite Gaussian directions on a deterministic quadratic "
                "compare the identity-corrected and rank-one forms."
            ),
            "limitation": raw_claims["C1_estimator_forms_proxy"]["limitation"],
        },
        {
            "id": "C2",
            "paper_claim": "Theorem 4.6: unbiasedness of the smoothed Hessian estimator",
            "status": "FINITE_ANALYTIC_PROXY",
            "raw_diagnostic": "C2_unbiasedness_proxy",
            "evidence": (
                "Finite baseline-difference scaling and convergence to analytic "
                "quadratic/quartic smoothed Hessians."
            ),
            "limitation": raw_claims["C2_unbiasedness_proxy"]["limitation"],
        },
        {
            "id": "C3",
            "paper_claim": "Theorems 4.7 and 4.8: baseline and bias-variance behavior",
            "status": "FINITE_BIAS_VARIANCE_PROXY",
            "raw_diagnostic": "C3_bias_variance_proxy",
            "evidence": (
                "Finite dimension trend for the optimal baseline, MSE decrease "
                "with K, and quartic smoothing-bias trend."
            ),
            "limitation": raw_claims["C3_bias_variance_proxy"]["limitation"],
        },
        {
            "id": "C4",
            "paper_claim": "Figure 2: ZoVH accuracy comparison",
            "status": "HONEST_NEGATIVE",
            "raw_diagnostic": "C4_central_difference_proxy",
            "evidence": (
                "At one fixed synthetic setting, the bare single-batch estimator "
                "has larger error than central differences."
            ),
            "limitation": raw_claims["C4_central_difference_proxy"]["limitation"],
        },
        {
            "id": "C5",
            "paper_claim": "Section 6.3: MNIST black-box adversarial attack",
            "status": "NOT_REPRODUCED",
            "raw_diagnostic": None,
            "evidence": "No MNIST data, attack implementation, or reported runs are present.",
            "limitation": (
                "The paper's query-reuse attack protocol and its comparison "
                "against Vanilla ZOO were not run."
            ),
        },
        {
            "id": "C6",
            "paper_claim": "Section 6.2: synthetic curvature-aware ZOO speedup",
            "status": "NOT_REPRODUCED",
            "raw_diagnostic": None,
            "evidence": "No optimizer, convergence curves, or speedup runs are present.",
            "limitation": (
                "The paper's full ZoVH optimizer, inverse-Hessian/product "
                "estimators, query reuse, and 22x comparison were not run."
            ),
        },
    ]

    claim_status = {claim["id"]: claim["status"] for claim in claims}
    report = {
        "paper": diagnostics["paper"],
        "authors": diagnostics["authors"],
        "arxiv": diagnostics["arxiv"],
        "openreview": diagnostics["openreview"],
        "scope": diagnostics["scope"],
        "overall_status": "INCONCLUSIVE",
        "paper_claims_verified": 0,
        "paper_claims_total": 6,
        "claims_not_reproduced": 2,
        "finite_proxy_diagnostics_passed": finite_passed,
        "finite_proxy_diagnostics_total": finite_total,
        "negative_diagnostics": 1,
        "claims": claims,
        "claim_status": claim_status,
        "attribution": "MachineLearning-Nerd",
    }
    gate = {
        **report,
        "tests_passed": tests_passed,
        "publication_gate_passed": tests_passed,
        "gate_meaning": (
            "Ready for the documented bounded proxy scope; this gate is not "
            "evidence that the six paper claims were reproduced."
        ),
        "verification_command": (
            "python3 repro/src/verify.py && "
            "python3 repro/src/finalize_gate.py"
        ),
    }

    for path in [
        os.path.join(OUTPUTS, "gate.json"),
        os.path.join(ROOT, "publication_gate.json"),
    ]:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(gate, handle, indent=2)
            handle.write("\n")

    print(f"Publication gate passed: {tests_passed}")
    print("Paper-level claims independently verified: 0/6")
    print(f"Finite proxy diagnostics passed: {finite_passed}/{finite_total}")
    print("Saved outputs/gate.json and publication_gate.json")


if __name__ == "__main__":
    main()
