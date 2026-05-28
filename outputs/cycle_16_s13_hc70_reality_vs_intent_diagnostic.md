# Cycle-16-S13 BE-H reality-vs-intent diagnostic (HC #70)

Per-piece honest table: claim / measured-vs-heuristic / probe-fire evidence ref / honest gap.

| Piece | Claim | tag | Probe-fire evidence ref | Honest gap |
|---|---|---|---|---|
| Substitution Gate (#14) | Refuses 3+ real proxy defs, passes 1 probe-ref def | [measured] | `outputs/structural_prevention_substitution_gate_events.jsonl` (3 refuse + 2 pass; EX1 drew real Cycle-16 proxies: BE-D 137-dormant citation-density, pre-Done#17 registry-field, emission-record) | Judges definitions *handed to it*; does not auto-scan all RQS/ED prose for un-passed defs |
| Stage-0 presence (#15a) | Halts if any required probe absent/fails self-test | [measured] | `outputs/structural_prevention_stage_0_probe_presence_events.jsonl` (pass 4/4; refuse on probes-dir-absent) | Hard-codes the 4 BE-F classes; new classes (E/F) need list update |
| Reality-vs-intent (#15b) | Refuses incomplete table; executes probe column | [measured] | `outputs/structural_prevention_reality_vs_intent_events.jsonl` (EX3 incomplete-row FAIL) | Validates table structure + probe self-test; does NOT verify the baseline number is itself measured |
| Number-tagging (#15c) | Blocks untagged + heuristic-in-verdict | [measured] | `outputs/structural_prevention_number_tagging_events.jsonl` (EX2 1 heuristic-in-verdict FAIL) | Regex primary-number detection is heuristic; edge cases in dense tables may over/under-match |
| Probe-coverage (#15d) | >=1 production fire per class; smoke excluded | [measured] | `outputs/structural_prevention_probe_coverage_events.jsonl` (a9/b10/c190/d59 prod impl 1/2/32/37) | "production" = run_id not `_smoke_`/`_self_test_`; relies on naming discipline, not cryptographic provenance |
| Library self-test (#15e) | Crash=fail; 2 consecutive=deprecate | [measured] | `outputs/probe_library_auto_deprecate_events.jsonl` (1 deprecation: probe_broken, prod run_id) + `probe_library_self_test_events.jsonl` (crash:true rows) | "2 consecutive sessions" partitioned by session string; depends on caller passing distinct `--session` |
| Deferral-expiration (#15f) | Refuses 3-of-4-field + expired | [measured] | `outputs/structural_prevention_deferral_expiration_events.jsonl` (EX4 missing reactivation_condition FAIL) | Reads a deferrals JSON handed to it; nothing forces the deferral registry to be the input |
| Design-anchor (#15g) | Refuses absent column; flags internal load-bearing | [measured] | `outputs/structural_prevention_design_anchor_disclosure_events.jsonl` (checkpoint_flag on internally-inherited four-gate skeleton) | Disclosure is self-reported; gate checks completeness, not honesty of the anchor tag |
| HC-BE-G-1 fix | Crash=fail-closed, not silent PASS=0 | [measured] | blocking crash run rc=1 "CRASH ... NOT coerced to PASS", silent-pass=0, BLOCKED=1; advisory run loud CRASH WARN silent-pass=0; clean run PASS 0 dormant | cycle_16 mirror ONLY; govML canonical copy still fail-open (BE-I carry) |
| HC-BE-G-2 fix | Real session partition, not `*64` | [measured] | live 5-session fixture run: gate flags 1 dormant spec with fires=3 (exactly last 3 distinct sessions s3,s4,s5); under magic-64 it would include all 5 rows -> 0 dormant. DIVERGE confirmed | cycle_16 mirror ONLY; govML copy carries magic-64 (BE-I carry) |

## HC #70 honest scope statement — what BE-H does NOT prove

BE-H ships PREVENTION machinery (gates that refuse the substitution failure mode
at its surfaces). BE-H does NOT:

- Validate the BE-F probes' own accuracy against independent blind-labeled ground
  truth — that is Done #25 / Phase 12 (KT-15). A passing probe self-test means it
  distinguishes its OWN fixtures, not that it measures reality correctly.
- Fix any past spec (Phases 11-13) or enumerate the defensible denominator (Done #27).
- Wire the gates into govML scaffolding so future cycles inherit them — that is
  BE-I (S14); ED §5.9 threshold 5 (init_project.sh integration) is N/A at S13.
- Force its own consumption: most gates judge inputs handed to them; the *binding*
  that these gates actually fire at each Stage surface is RP-fill + orchestration
  scope, not a property BE-H self-proves.
- Back-port the two carry fixes to the govML canonical session_close_gate copy
  (still fail-open + magic-64 there; BE-I carry).
