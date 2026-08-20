#!/usr/bin/env python3
"""Verify the published ZoVH bounded-audit contract."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_IDENTITY = (
    "MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>"
)
EXPECTED_RECOVERY_SHA = (
    "3817d3b55118ea1cb61f819d7898d4634339e8a328effbe7761c5bfe33b1b978"
)
EXPECTED_SOURCE_TIP = "f39b869df88639cd2028cee2a95444f4b74319c3"
EXPECTED_STATUS = (
    "INCONCLUSIVE_C1_ALGEBRAIC_FINITE_PROXY_"
    "C2_FINITE_ANALYTIC_PROXY_C3_FINITE_BIAS_VARIANCE_PROXY_"
    "C4_HONEST_NEGATIVE_C5_C6_NOT_REPRODUCED_"
    "NO_PAPER_CLAIMS_VERIFIED_NO_CURRENT_SCORE"
)
EXPECTED_CLAIMS = {
    "C1": "ALGEBRAIC_FINITE_PROXY",
    "C2": "FINITE_ANALYTIC_PROXY",
    "C3": "FINITE_BIAS_VARIANCE_PROXY",
    "C4": "HONEST_NEGATIVE",
    "C5": "NOT_REPRODUCED",
    "C6": "NOT_REPRODUCED",
}


def fail(reason: str) -> None:
    print("FINAL_AUDIT=FAILED reason=" + reason)
    raise SystemExit(1)


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        fail("git_" + "_".join(args))
    return result.stdout.strip()


def load(relative_path: str) -> dict:
    try:
        with (ROOT / relative_path).open(encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        fail(relative_path + "_invalid_" + type(error).__name__)
    raise AssertionError("unreachable")


local_heads = {
    line
    for line in git(
        "for-each-ref",
        "refs/heads",
        "--format=%(refname:short)",
    ).splitlines()
    if line
}
if local_heads != {"main"}:
    fail("branches_" + ",".join(sorted(local_heads)))
if git("branch", "--show-current") != "main":
    fail("head_not_main")

remote_heads = {
    line.removeprefix("origin/")
    for line in git(
        "for-each-ref",
        "refs/remotes/origin",
        "--format=%(refname:short)",
    ).splitlines()
    if line and line != "origin"
}
if remote_heads and remote_heads != {"main"}:
    fail("remote_branches_" + ",".join(sorted(remote_heads)))

all_refs = git("for-each-ref", "--format=%(refname)").splitlines()
if any(
    ref.endswith("/master")
    or "/orx/" in ref
    or ref.endswith("/orx")
    for ref in all_refs
):
    fail("legacy_branch_ref")

commit_count = int(git("rev-list", "--count", "--all"))
if commit_count < 4:
    fail("commit_count_" + str(commit_count))

identity_rows = git(
    "log",
    "--all",
    "--format=%an <%ae>|%cn <%ce>",
).splitlines()
expected_row = EXPECTED_IDENTITY + "|" + EXPECTED_IDENTITY
if not identity_rows or any(row != expected_row for row in identity_rows):
    fail("noncanonical_commit_identity")

claims_doc = load("claims.json")
claims = {claim["id"]: claim for claim in claims_doc["claims"]}
if set(claims) != set(EXPECTED_CLAIMS):
    fail("claim_ids")
if {
    claim_id: claims[claim_id]["status"]
    for claim_id in EXPECTED_CLAIMS
} != EXPECTED_CLAIMS:
    fail("claim_statuses")
if claims_doc.get("overall_status") != EXPECTED_STATUS:
    fail("claims_status")

audit = claims_doc.get("audit", {})
for field, expected in (
    ("finite_proxy_diagnostics_passed", 3),
    ("finite_proxy_diagnostics_total", 4),
    ("negative_diagnostics", 1),
    ("claims_not_reproduced", 2),
    ("paper_claims_not_verified", 6),
    ("claims_total", 6),
    ("evidence_points", 8),
    ("evidence_points_total", 12),
    ("paper_claims_verified", 0),
):
    if audit.get(field) != expected:
        fail("claims_" + field)
for field in ("current_score_claim", "publication_allowed"):
    if audit.get(field) is not False:
        fail("claims_" + field)

verdict = load("outputs/verdict.json")
if verdict.get("overall_status") != EXPECTED_STATUS:
    fail("verdict_status")
if verdict.get("paper_reproduction") != "inconclusive":
    fail("verdict_paper_reproduction")
for field, expected in (
    ("claims_total", 6),
    ("finite_proxy_diagnostics_passed", 3),
    ("finite_proxy_diagnostics_total", 4),
    ("negative_diagnostics", 1),
    ("claims_not_reproduced", 2),
    ("paper_claims_not_verified", 6),
    ("evidence_points", 8),
    ("evidence_points_total", 12),
    ("paper_claims_verified", 0),
):
    if verdict.get(field) != expected:
        fail("verdict_" + field)
for field in ("current_score_claim", "publication_allowed"):
    if verdict.get(field) is not False:
        fail("verdict_" + field)
if verdict.get("claim_status") != EXPECTED_CLAIMS:
    fail("verdict_claim_status")

verdict_claims = {claim["id"]: claim for claim in verdict.get("claims", [])}
for claim_id, expected_status in EXPECTED_CLAIMS.items():
    if verdict_claims.get(claim_id, {}).get("status") != expected_status:
        fail("verdict_" + claim_id)
    if verdict_claims.get(claim_id, {}).get("paper_claim_reproduced") is not False:
        fail("verdict_" + claim_id + "_paper_claim")

diagnostics = load("outputs/diagnostics.json")
expected_diagnostic_keys = {
    "C1_estimator_forms_proxy",
    "C2_unbiasedness_proxy",
    "C3_bias_variance_proxy",
    "C4_central_difference_proxy",
}
if set(diagnostics.get("claims", {})) != expected_diagnostic_keys:
    fail("diagnostic_keys")
expected_diagnostic_statuses = {
    "C1_estimator_forms_proxy": ("ALGEBRAIC_FINITE_PROXY", True),
    "C2_unbiasedness_proxy": ("FINITE_ANALYTIC_PROXY", True),
    "C3_bias_variance_proxy": ("FINITE_BIAS_VARIANCE_PROXY", True),
    "C4_central_difference_proxy": ("HONEST_NEGATIVE", False),
}
for key, (expected_status, expected_pass) in expected_diagnostic_statuses.items():
    diagnostic = diagnostics["claims"][key]
    if diagnostic.get("status") != expected_status:
        fail("diagnostic_" + key)
    if diagnostic.get("finite_proxy_passed") is not expected_pass:
        fail("diagnostic_" + key + "_pass")

gate = load("outputs/gate.json")
for field in ("tests_passed", "documentation_gate_passed", "publication_gate_passed"):
    if gate.get(field) is not True:
        fail("gate_" + field)
for field in (
    "paper_reproduction_gate_passed",
    "paper_algorithm_implemented",
    "paper_claims_reproduced",
    "current_score_claim",
    "publication_allowed",
):
    if gate.get(field) is not False:
        fail("gate_" + field)
for field, expected in (
    ("claims_total", 6),
    ("finite_proxy_diagnostics_passed", 3),
    ("finite_proxy_diagnostics_total", 4),
    ("negative_diagnostics", 1),
    ("claims_not_reproduced", 2),
    ("paper_claims_not_verified", 6),
    ("evidence_points", 8),
    ("evidence_points_total", 12),
    ("paper_claims_verified", 0),
):
    if gate.get(field) != expected:
        fail("gate_" + field)
if gate.get("overall_status") != EXPECTED_STATUS:
    fail("gate_status")

publication_gate = load("publication_gate.json")
if publication_gate.get("paper_reproduction_gate_passed") is not False:
    fail("publication_paper_gate")
if publication_gate.get("publication_allowed") is not False:
    fail("publication_allowed")
if publication_gate.get("overall_status") != EXPECTED_STATUS:
    fail("publication_status")

verdicts = load("reproduction_verdicts.json")
if verdicts.get("claim_statuses") != EXPECTED_CLAIMS:
    fail("reproduction_claim_statuses")
if verdicts.get("evidence", {}).get("paper_claims_verified") != 0:
    fail("reproduction_paper_claims")
if verdicts.get("evidence", {}).get("evidence_points") != 8:
    fail("reproduction_evidence_points")

state = load("AUTONOMOUS_STATE.json")
if state.get("status") != EXPECTED_STATUS:
    fail("state_status")
if state.get("repository", {}).get("recovery_bundle_sha256") != EXPECTED_RECOVERY_SHA:
    fail("state_recovery_sha")
if state.get("repository", {}).get("canonical_email") != (
    "MachineLearning-Nerd@users.noreply.github.com"
):
    fail("state_identity")
if state.get("source", {}).get("source_tip_before_standardization") != EXPECTED_SOURCE_TIP:
    fail("state_source_tip")

manifest = load("EVIDENCE_MANIFEST.json")
missing = [
    path
    for path in manifest["required_paths"]
    if not (ROOT / path).is_file()
]
if missing:
    fail("missing_paths_" + ",".join(missing))

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for marker in (
    "2605.30960",
    "CLAIM_EVIDENCE.md",
    "Thank you",
    "0/6",
    "HONEST_NEGATIVE",
    "MachineLearning-Nerd",
):
    if marker not in readme:
        fail("readme_" + marker.replace(" ", "_"))

branch_audit = (ROOT / "BRANCH_AUDIT.md").read_text(encoding="utf-8")
for marker in (EXPECTED_IDENTITY, EXPECTED_SOURCE_TIP, EXPECTED_RECOVERY_SHA):
    if marker not in branch_audit:
        fail("branch_audit_" + marker[:12])

print(
    "FINAL_AUDIT=VERIFIED "
    "branches=1 commits="
    + str(commit_count)
    + " claims=C1:algebraic_proxy,C2:analytic_proxy,C3:bias_variance_proxy,"
    + "C4:honest_negative,C5:C6:not_reproduced "
    + "evidence_points=8 paper_claims_verified=0 current_score_claim=false "
    + "publication_allowed=false"
)
