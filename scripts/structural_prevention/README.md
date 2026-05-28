# BE-H structural-prevention layer (Cycle-16-S13)

Eight structural-prevention mechanisms that prevent the operational-definition
substitution failure mode (Cycle 9+ meta-failure) at its surfaces. Each gate
that judges implementation IMPORTS + `subprocess`-executes a named BE-F probe
primitive (`scripts/probes/{a,b,c,d}/probe_*.py`) and reads real probe-fire
evidence — never string-matching a probe ID, status enum, token count, or
"file exists at path" (KT-8 BINDING).

## Mechanisms

| File | Done | Fires at | Refuses |
|---|---|---|---|
| `operational_definition_substitution_gate.py` | #14 | Stage 1 RQS close + Stage 4 ED/ACCEPTANCE close | proxy definition with no executable probe reference |
| `stage_0_probe_presence_check.sh` | #15a | before Stage 1 entry | any required probe absent or failing self-test |
| `reality_vs_intent_gate.py` | #15b | Stage 1 RQS R3 + Stage 4 ED R3 | missing/incomplete 4-column intent table |
| `number_tagging_gate.py` | #15c | FINDINGS / close summaries / transition prompts / handoffs | untagged primary number + [heuristic] number in a Done verdict |
| `probe_coverage_check.sh` | #15d | FINDINGS close | any governed class with 0 PRODUCTION fires (smoke excluded) |
| `library_self_test_gate.sh` | #15e | session close | crashing probe (HC-BE-G-1 tie) + 2-consecutive-fail auto-deprecate |
| `deferral_expiration_gate.py` | #15f | deferral creation / cycle close | deferral missing any of 4 fields or past its dormancy window |
| `design_anchor_disclosure_gate.py` | #15g | LANDSCAPE close | absent disclosure column; flags internally-inherited load-bearing design |

Every mechanism: shebang + DP#44 refuse-on-missing-precondition + a dedicated
`outputs/structural_prevention_<piece>_events.jsonl` sink (>=1 `*.refuse.event`
+ >=1 `*.pass.event`). Production run_ids use the `s13_be_h_production_*` prefix.

Pieces #15c (number-tagging), #15f (deferral), #15g (design-anchor) judge
text/JSON *structure* (a Rex-facing surface or a self-reported enumeration), not
running code, so they carry no probe-subprocess predicate by design; KT-8 applies
to the 5 implementation-judging predicates (#14/#15a/#15b/#15d/#15e).

## BE-I / S14 govML back-port — DECLARED integration-function signature

ED §5.9 names govML paths. Per the kc-49 evidence-path-translation disposition
this layer ships at the cycle_16 first-arc; the govML back-port is BE-I (S14).
ED §5.9 threshold 5 (init_project.sh integration + scaffold materialization) is
**N/A at S13**. The integration-function signature to be wired at BE-I:

```bash
# in ~/ml-governance-templates/scripts/init_project.sh (BE-I / S14):
install_structural_prevention_layer "<project_dir>"
#   - copies scripts/structural_prevention/*.{sh,py} into the scaffolded project
#   - back-ports the HC-BE-G-1 fail-closed dormancy + HC-BE-G-2 real session
#     partition into the canonical scripts/be_g_mirror copy (still fail-open +
#     magic-64 in govML v2.8.5 — BE-I carry)
#   - VERSION bump v2.8.5 -> v2.8.6 (ADDITIVE-APPEND chain extension to n=6)
#   - LOCKED bodies of the 5 prior install_* functions UNMODIFIED (KT-11 guard)
```

govML stays v2.8.5 this session — NOT touched at S13.
