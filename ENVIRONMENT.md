# Environment and execution contract

## Canonical commands

The publication contract consumes the existing raw diagnostic output:

~~~bash
python3 repro/src/finalize_gate.py
python3 verify_final.py
~~~

The first command formats outputs/diagnostics.json into the canonical verdict
and gate. The second checks files, claim statuses, branches, attribution, and
publication flags. The scientific runner repro/src/verify.py is retained for
provenance and is not required for the documentation contract.

## Runtime boundary

- The existing finite helpers use Python 3 and NumPy.
- No GPU, MNIST data, author package, or paper-scale benchmark is assumed.
- Numeric values are existing finite measurements, not theorem guarantees.
- The negative C4 result is retained; it is not silently replaced by a
  stronger paper claim.

If the raw diagnostic output changes, regenerate the ledger and rerun
verify_final.py. Do not hand-edit a proxy into a paper-level result.
