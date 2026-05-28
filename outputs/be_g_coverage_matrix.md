# BE-G Per-Repo Enforcement Coverage Matrix (Done #29)

Authority: BE-G dispatch substrate §2 item 8 (SI Amendment 28d Done #29) + ED §5.8.
Session: Cycle-16-S12. Companion machine-readable: `be_g_coverage_matrix.json`.

## Scope honesty (HC #70)

The build SHIPS the enforcement mechanism (pre-commit hook + fsnotify watcher +
3-registry reconciliation gate + CI required-status-check spec) AND this per-repo
matrix. INSTALLING the hook into each repo's `.git/hooks/pre-commit` and wiring the
CI required check into branch protection is an **operational promotion step**, not
something the build silently performs across all repos. The matrix enumerates every
spec-bearing repo with its per-repo mechanism; it does NOT claim hooks are already
live in 79 repos.

## `--no-verify` bypass closure (the load-bearing Done #29 piece)

A local `pre-commit` hook is bypassable with `git commit --no-verify`. A local hook
on one repo is therefore **NOT** acceptance. Closure requires a **server-side / CI
required-status-check**: `.github/workflows/spec_authoring_required_check.yml` runs
the hook predicate (`spec_authoring_pre_commit_hook.sh --check-staged`) against the
PR diff and is registered as a **required status check** under branch protection. CI
required checks cannot be `--no-verify`'d — the bypass is closed at the server.

## Matrix

| Repo | On disk | Agent specs | Schemas | Local hook | Watcher | Reconciliation | Bypass closure (server-side/CI) |
|---|---|---|---|---|---|---|---|
| Moonshots_Career_Thesis_v2 | yes | 9 | 0 | `spec_authoring_pre_commit_hook.sh` (symlink as `.git/hooks/pre-commit`) | `spec_authoring_watcher.py` daemon | `three_registry_reconciliation_gate.sh` | `.github/workflows/spec_authoring_required_check.yml` (required status check) |
| cycle_16_close_spec_to_implementation_gap_build | yes | 0 | 2 | same hook | same watcher | same gate | same CI required check |
| ml-governance-templates (govML) | yes | 0 | 2 | same hook | same watcher | same gate | same CI required check |
| emabs_moonshots (EMABS) | no (mirror; Coach-managed per PC #100) | — | — | n/a until materialized | n/a until materialized | inherits gate when materialized | inherits CI required-check spec when materialized |

Cycle_N build repos (cycle_10..cycle_16) are spec-bearing during their active cycle;
each inherits the same installable mechanism via the govML `init_project.sh` install
path (back-port of the BE-G scripts to govML is BE-I / S14, NOT done at S12).

## Mechanism source paths

- Pre-commit hook: `~/ml-governance-templates/scripts/spec_authoring_pre_commit_hook.sh`
- Watcher: `~/ml-governance-templates/scripts/spec_authoring_watcher.py`
- Reconciliation gate: `~/ml-governance-templates/scripts/three_registry_reconciliation_gate.sh`
- CI required-check workflow (spec/template): `outputs/spec_authoring_required_check.yml`
  (the workflow file shipped as a deliverable; installed into each repo's
  `.github/workflows/` at promotion).
