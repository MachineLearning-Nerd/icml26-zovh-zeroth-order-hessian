# verify

## Command

~~~bash
python3 repro/src/verify.py
python3 repro/src/finalize_gate.py
~~~

## Interpretation

The verifier writes raw finite measurements to outputs/diagnostics.json. The finalizer maps those measurements onto the six paper claims and writes outputs/gate.json.

The finite diagnostic result is **3/4 passed**, with C4 an honest negative. The paper-level result is **0/6 independently verified** because C1–C3 are explicitly bounded proxies and C5–C6 were not run.

## Important scope boundary

The paper’s headline empirical gains depend on the full ZoVH implementation: query reuse, variance-reduced baselines, inverse-Hessian/product estimators, the curvature-aware optimizer, and application-specific experiments. None of those absent components are inferred from the toy diagnostics.
