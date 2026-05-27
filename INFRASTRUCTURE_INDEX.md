# Infrastructure Index — cycle_16_close_spec_to_implementation_gap_build

> **Auto-generated** by `~/ml-governance-templates/scripts/gen_infrastructure_index.py`.
> Re-run via `<project>/scripts/run_index.sh` (scaffolded by `scaffold_research_project.py`).
> **Idempotent:** byte-identical output across re-runs for unchanged project state.

## Project Metadata

| Field | Value |
| --- | --- |
| project | cycle_16_close_spec_to_implementation_gap_build |
| research_type | build |
| profile | research-build |
| quality_target | 8.0 |
| sharing_tier | 3 |

## F-C Discoverability Sub-Mechanism — Path B Static Markdown Analog

Per `research_infrastructure_discoverability_and_enforcement` cycle 1 Risk Register row 1 fallback authorization:
MCP server full build (Path A) is deferred to Phase 1.5+ as a forward candidate.
This static markdown index serves as the LSP-analog discoverability surface (per LA §1 row 9) at lower
engineering cost. The MCP-as-protocol upgrade path remains open via `capability_option 49` in
`singularity.db v_question_inputs` (synergy_score 8.5).

## govML Scripts (Applicable per research_type=build)

Located at `~/ml-governance-templates/scripts/`. Reference-by-shim convention (no body duplication).

| Script | Purpose |
| --- | --- |
| landscape_depth_gate_F3.sh | F3 composite runner — landscape depth gate (Stage 2) |
| landscape_depth_gate.sh | F1 structural pre-filter — landscape depth |
| landscape_depth_judge.py | F2 LLM-judge — landscape depth |
| pre_compute_check.sh | Pre-compute precondition check (pre-Phase-1) |
| check_all_gates.sh | Run all govML gates (post-Phase-1) |
| quality_loop.sh | Quality scoring loop — T3 dimension scoring (Phase 3) |
| semantic_review.py | Semantic G24 review (Phase 3) |
| preflight_findings.sh | Preflight FINDINGS check (Phase 3) |
| gen_findings_audit.py | FINDINGS audit generator (N/PS/BS/G sections) |
| gen_hypothesis_registry.py | Hypothesis registry generator |
| check_generalizability.sh | Cross-domain generalizability check |
| check_paper_structure.sh | Paper-structure compliance check |

## Pipeline Gates (Stage 0-2 Transitions)

Located at `~/Moonshots_Career_Thesis_v2/scripts/`. Fire at stage transitions.

| Gate | Purpose |
| --- | --- |
| scripts/observation_gate.sh | Stage 0 → Stage 1 transition gate (OBSERVATION_LOG.md) |
| scripts/question_gate.sh | Stage 1 → Stage 2 transition gate (RESEARCH_QUESTION_SPEC.md) |
| scripts/landscape_gate.sh | Stage 2 → Stage 3 transition gate (LANDSCAPE_ASSESSMENT.md) |

## Agent Specs (5 active)

Located at `~/Moonshots_Career_Thesis_v2/.claude/agents/`. Authoritative for each agent's workflow.

| Spec | Scope |
| --- | --- |
| .claude/agents/research-orchestrator.md | Stages 0-4 orchestrator (Researcher-Planner dispatch) |
| .claude/agents/research-researcher-planner.md | Stages 0-4 RP — fills OBS/RQS/LA + ED §0-§4 + PROJECT/REQUIREMENTS/HR/ROADMAP |
| .claude/agents/execution-orchestrator.md | Stage 5 orchestrator — Execute → Verify → Handoff (FINDINGS-producing) |
| .claude/agents/research-executor.md | Stage 5 Executor — produces FINDINGS.md |
| .claude/agents/research-verifier.md | Stage 5 Verifier — independently verifies FINDINGS against rubric |

## govML Templates

Located at `~/ml-governance-templates/templates/`. Per-subdir listing:

### `core/` (31 files)

- `ADVERSARIAL_EVALUATION.tmpl.md`
- `AI_DIVISION_OF_LABOR.tmpl.md`
- `ARTIFACT_MANIFEST_SPEC.tmpl.md`
- `ARTIFACT_PACKAGING.tmpl.md`
- `A_PLUS_CHECKLIST.tmpl.md`
- `A_PLUS_CHECKLIST_SIMULATION.tmpl.md`
- `BUILD_SYSTEM_CONTRACT.tmpl.md`
- `CLAIM_STRENGTH_SPEC.tmpl.md`
- `COMPUTATIONAL_COST_SPEC.tmpl.md`
- `CONCURRENCY_TESTING_SPEC.tmpl.md`
- `CONFIGURATION_SPEC.tmpl.md`
- `DATA_CONTRACT.tmpl.md`
- `DECISION_LOG.tmpl.md`
- `ENVIRONMENT_CONTRACT.tmpl.md`
- `ENVIRONMENT_SPEC.tmpl.md`
- `EXECUTION_PROTOCOL.tmpl.md`
- `EXPERIMENTAL_DESIGN.tmpl.md`
- `EXPERIMENT_CONTRACT.tmpl.md`
- `FIGURES_TABLES_CONTRACT.tmpl.md`
- `FINDINGS.tmpl.md`
- `HYPOTHESIS_CONTRACT.tmpl.md`
- `HYPOTHESIS_REGISTRY.tmpl.md`
- `LEARNING_CURVE_SPEC.tmpl.md`
- `METRICS_CONTRACT.tmpl.md`
- `MODEL_COMPLEXITY_SPEC.tmpl.md`
- `PERFORMANCE_BENCHMARKING_SPEC.tmpl.md`
- `PROVENANCE_SPEC.tmpl.md`
- `SANITY_BASELINE_SPEC.tmpl.md`
- `SCRIPT_ENTRYPOINTS_SPEC.tmpl.md`
- `STATISTICAL_ANALYSIS_SPEC.tmpl.md`
- `TEST_ARCHITECTURE.tmpl.md`

### `management/` (7 files)

- `CHANGELOG.tmpl.md`
- `CLAUDE_MD.tmpl.md`
- `DECISION_LOG.tmpl.md`
- `IMPLEMENTATION_PLAYBOOK.tmpl.md`
- `PRIOR_WORK_REUSE.tmpl.md`
- `RISK_REGISTER.tmpl.md`
- `TASK_BOARD.tmpl.md`

### `publishing/` (25 files)

- `ACADEMIC_INTEGRITY_FIREWALL.tmpl.md`
- `ARTIFACT_EVALUATION_SPEC.tmpl.md`
- `AUTHOR_CONTRIBUTIONS.tmpl.md`
- `BROADER_IMPACT_STATEMENT.tmpl.md`
- `COI_DISCLOSURE.tmpl.md`
- `CONTENT_PLAN.tmpl.md`
- `DATA_AVAILABILITY_STATEMENT.tmpl.md`
- `ETHICS_STATEMENT.tmpl.md`
- `IMAGE_BRIEF.tmpl.md`
- `LEAN_HYPOTHESIS.tmpl.md`
- `NEWSLETTER_CLARITY_AUDIT.tmpl.md`
- `NEWSLETTER_FORMAT.tmpl.md`
- `NEWSLETTER_RESEARCH.tmpl.md`
- `NEWSLETTER_RUBRIC.tmpl.md`
- `NEWSLETTER_VOICE.tmpl.md`
- `PROJECT_BRIEF.tmpl.md`
- `PUBLICATION_BRIEF.tmpl.md`
- `PUBLICATION_PIPELINE.tmpl.md`
- `README.tmpl.md`
- `REGULAR_POST_CLARITY_AUDIT.tmpl.md`
- `REGULAR_POST_FORMAT.tmpl.md`
- `REGULAR_POST_RUBRIC.tmpl.md`
- `REGULAR_POST_VOICE.tmpl.md`
- `REVIEW_LOG.tmpl.md`
- `THREATS_TO_VALIDITY.tmpl.md`

### `report/` (8 files)

- `EXECUTION_MANIFEST.tmpl.md`
- `PHASE_AUDIT.tmpl.md`
- `PRE_SUBMISSION_CHECKLIST.tmpl.md`
- `REPORT_ASSEMBLY_PLAN.tmpl.md`
- `REPORT_CONSISTENCY_SPEC.tmpl.md`
- `REPRODUCIBILITY_SPEC.tmpl.md`
- `RUBRIC_TRACEABILITY.tmpl.md`
- `SUBMISSION_BRANCH_SPEC.tmpl.md`

### `strategy/` (3 files)

- `LANDSCAPE_ASSESSMENT.tmpl.md`
- `OBSERVATION_LOG.tmpl.md`
- `RESEARCH_QUESTION_SPEC.tmpl.md`

## Memory Entries (50 active)

Located at `~/.claude/projects/-home-azureuser-Moonshots-Career-Thesis-v2/memory/`.
Routing schema at `MEMORY_ROUTING.md` (decision-context bindings).

| Entry | Description |
| --- | --- |
| `feedback_blast_radius_anti_pattern.md` | S120 n=3, S137 n=9, S138 evaluator n=2 (arc total n=11 as of 2026-04-22). Coaches (and evaluators) invoke downstream imp |
| `feedback_builders_not_subagents.md` | Builder sessions are separate Claude Code sessions with warmup/protocol — never use Agent tool as Builder substitute |
| `feedback_check_si_before_directing_rex.md` | "Before directing any timing-bound or checkpoint-bound work to Rex (especially items framed as \"between S_N close and S |
| `feedback_coach_handoffs_selfsufficient.md` | handoff.md must contain 8 mandatory sections so Rex never needs a custom Coach prompt. "Follow the warmup protocol" is e |
| `feedback_coach_substrate_pattern.md` | When a subagent dispatch is compose-bound at ~30K+ chars (stream-watchdog stall class), Coach `cp` of canonical template |
| `feedback_context_reporting.md` | Report files read/written, not percentages or qualitative labels. Rex judges context state. |
| `feedback_data_substrate_freshness_verification.md` | At Stage 3-4 design, before pre-registering hypotheses + constraints derived from a pre-existing data file, confirm the  |
| `feedback_depth_matches_complexity.md` | For unfamiliar systems >500 lines, require ~70% research before any fix proposals. Fix size ≠ required understanding. |
| `feedback_depth_over_speed.md` | Research agents ignore time budgets (60 min budget, 3 min execution). Use depth requirements (quote N sources, read N fu |
| `feedback_email_domain_fte_check.md` | When someone follows up via email after a call, the email domain reveals FTE-vs-consultant status in 30 seconds. If doma |
| `feedback_evaluator_role_boundary.md` | Evaluator (Coach's Coach) role is independent review via Path B. Caught 3x in S120 crossing the boundary — wrote dispatc |
| `feedback_executive_plan_summary_sources.md` | "Before answering \"what is the plan\" / \"what cycles come after this\" / \"walk me through the program\" / any cycle-a |
| `feedback_fetch_agents_fail.md` | Agents that rely on WebFetch tend to hang and get rejected. Use WebSearch-first approaches. Do research directly when po |
| `feedback_fetch_mitigation_not_verified.md` | Fallback chain language added to Executor spec but autonomous 30-second abandon behavior never tested. Rex intervened ma |
| `feedback_honest_evaluation.md` | Self-scoring has dual bias (generous initially, overcorrects when challenged). Always use blind evaluation for research  |
| `feedback_hypothesized_products_are_placeholders.md` | AgentArmor/SkillVet/RedClaw are paper-stage placeholder bucket-names with no fleshed-out hypothesis. Coach must not trea |
| `feedback_inbound_founder_call_playbook.md` | When Rex has an inbound call from a newsletter reader / founder / practitioner, fire 4 artifacts: research dossier → str |
| `feedback_kernel_coach_narrow_refix_overreach.md` | Kernel-coach must NOT drift into narrow re-fix discipline at typographical audit-trail level — block-on-substantive / fl |
| `feedback_kernel_coach_observe_then_direct.md` | kernel-coach writes only the one-line startup; task context / BEGIN PROMPT blocks come AFTER the coach's warmup check-ba |
| `feedback_linkedin_identification_limits.md` | Identifying a person by first name + company alone via public web search has a high failure rate. LinkedIn profiles 404  |
| `feedback_mistakes_inline.md` | All mistake prevention statements must be inline in warmup output, not just in the warmup file — Rex can't spot-check a  |
| `feedback_newsletter_no_body_cta.md` | In-body share CTAs must link directly to LinkedIn share-offsite (subscribers never leave linkedin.com). No rexcoleman.de |
| `feedback_no_idle_prompts.md` | "Don't write paste-ready prompts at turns where there is nothing to paste to a coach — kernel-coach Discipline" |
| `feedback_no_sleep_remarks.md` | Don't add "sleep well", "good night", or any time-of-day commentary to session-end summaries. Caught twice in same sessi |
| `feedback_phase_scope_discipline.md` | Rex correction S153 — stop surfacing carried items that are out of scope for the current research phase, even if handoff |
| `feedback_problem_statement_first.md` | When Rex asks "what is the plan" or for a status summary, lead with the problem being solved BEFORE describing the mecha |
| `feedback_prompt_brackets.md` | When writing a prompt for Rex to send to another session/agent, bracket the prompt body with `BEGIN PROMPT` and `END PRO |
| `feedback_prompts_are_governed.md` | Builder task prompts need version tracking, audit after protocol changes, Coach authorship. Track in prompt_inventory ta |
| `feedback_protocol_supersedes_pre_registered_surface.md` | When a transition prompt §Open paradigm questions row pre-registers a "Rex-disposition surface" but the research process |
| `feedback_recovery_options_are_operational.md` | When diagnosis surfaces multiple recovery options, 1 forbidden, 1 deferral-disposition, the sequence is mechanical (chea |
| `feedback_research_executor_rejected.md` | research-executor subagent type consistently gets rejected by user — use general-purpose instead |
| `feedback_rex_step_3_5_draft_for_approval.md` | "Rex does NOT author strategic frame items (Bindings, paradigm rulings, SI sections) from scratch. We converse; kernel-c |
| `feedback_session_rampup.md` | Rex uses a 5-step conversational ramp-up before giving tasks. Don't treat ramp-up questions as tasks. Demonstrate unders |
| `feedback_stop_asking_permission.md` | Coach repeatedly asked Rex to confirm operational steps (commit, proceed, approve). Rex's role is strategic — Coach shou |
| `feedback_strategic_vs_operational.md` | Coaches and persistent evaluators must route only paradigm/strategic decisions to Rex. Operational decisions (research t |
| `feedback_strictly_process_guided.md` | Rex S155 directive — research process and infrastructure are the rail; no Coach-direct overrides, no §11-style addenda,  |
| `feedback_thorough_schema_enumeration_before_unavailability_claim.md` | When an API exposes auth + some operations but a desired primitive appears absent from docs, do thorough automated enume |
| `feedback_verifier_must_exercise_live_api.md` | When verifying Coach close summaries about scripts that integrate with external APIs (Buffer, LinkedIn, GitHub, etc.), t |
| `feedback_webfetch_github.md` | WebFetch on github.com URLs consistently gets stuck/rejected. Use gh CLI or WebSearch instead. |
| `feedback_webfetch_slow.md` | WebFetch works for full-source research on most domains but fails on some (TLS errors). Use WebSearch for discovery, Web |
| `project_agent_architecture_status.md` | Three layers of agent architecture — v0 legacy (archived), v2 pipeline (likely legacy), Level 4 (current E2 build) |
| `project_bus_sub_route_a.md` | Operational pattern for invoking research-researcher-planner when research-orchestrator subagent harness lacks Task/Agen |
| `project_level4_research_engine.md` | Phases A-F complete, G-prep complete (S63). Signal pipeline operational (151 signals, 7 sources, cron). Phase G (autonom |
| `project_phase_c_architecture.md` | Rex reframed Phase C from "pick multi-agent framework" to "where is value add vs commodity?" — 3 layers, 3 paths propose |
| `project_s120_handoff_state.md` | Session closed 2026-04-17 late night. Track A SE-184 audit at Phase 3 + corrections PASS. Track C local-LLM at Phase 3 w |
| `reference_cycle_arc_canonical_sources.md` | "Canonical sources for the program's per-cycle scope definitions (Cycle N+1 through cycle-end). Read these before any ex |
| `reference_gpd_architecture.md` | PSI's open-source research agent system — 23 agents, 61 workflows, most sophisticated research agent architecture found. |
| `reference_linkedin_newsletter_url.md` | Stable LinkedIn URL for "Securing AI That Ships" newsletter. Used as share target in in-body CTAs (per-issue URLs are on |
| `reference_mac_mini_specs.md` | Authoritative Mac Mini hardware specs. Pointer to compute_resources DB + runbook. Operating mode 2026-05-06: GPU-science |
| `user_rex_strengths.md` | Rex excels at architectural/meta judgment (top quartile/1% grad school), NOT paper quality scoring. Remove Rex from rese |

## Per-Stage Quick Reference

### Stage 0 (Observe)

- scripts/observation_gate.sh (transition gate to Stage 1)
- .claude/agents/research-orchestrator.md + research-researcher-planner.md
- Templates: strategy/OBSERVATION_LOG.tmpl.md

### Stage 1 (Question)

- scripts/question_gate.sh (transition gate to Stage 2)
- .claude/agents/research-researcher-planner.md
- Templates: strategy/RESEARCH_QUESTION_SPEC.tmpl.md

### Stage 2 (Landscape)

- scripts/landscape_gate.sh (transition gate to Stage 3)
- ~/ml-governance-templates/scripts/landscape_depth_gate_F3.sh (F3 composite — depth check on LA)
- .claude/agents/research-researcher-planner.md
- Templates: strategy/LANDSCAPE_ASSESSMENT.tmpl.md

### Stage 3-4 (Hypothesize + Design)

- .claude/agents/research-orchestrator.md + research-researcher-planner.md
- Templates: core/EXPERIMENTAL_DESIGN.tmpl.md, core/HYPOTHESIS_REGISTRY.tmpl.md
- Required artifacts: PROJECT.md, REQUIREMENTS.md, ROADMAP.md (RP-filled per Stage 3-4)

### Stage 5 (Execute → Verify → Handoff)

- ~/ml-governance-templates/scripts/pre_compute_check.sh (precondition gate)
- .claude/agents/execution-orchestrator.md + research-executor.md + research-verifier.md
- Required artifact: FINDINGS.md (FINDINGS-producing single-pass Executor per agent spec)
- ~/ml-governance-templates/scripts/check_all_gates.sh + quality_loop.sh + semantic_review.py (post-Execute scoring)

## Invocation Contract (for `scaffold_research_project.py` extension)

- **Filename:** `INFRASTRUCTURE_INDEX.md` at project root.
- **Generator:** `~/ml-governance-templates/scripts/gen_infrastructure_index.py`
- **CLI:** `python3 gen_infrastructure_index.py --project <project_path> [--output <output_path>]`
- **Exit codes:** 0 = success; 1 = governance.yaml not found/unparseable; 2 = output write failed.
- **Idempotent:** re-running produces byte-identical output for unchanged project state (md5sum match).
- **Scaffolded shim:** `<project>/scripts/run_index.sh` (created by scaffold_research_project.py).

## Idempotency Verification Recipe

```bash
python3 ~/ml-governance-templates/scripts/gen_infrastructure_index.py --project /home/azureuser/cycle_16_close_spec_to_implementation_gap_build
md5sum INFRASTRUCTURE_INDEX.md > /tmp/before.md5
python3 ~/ml-governance-templates/scripts/gen_infrastructure_index.py --project /home/azureuser/cycle_16_close_spec_to_implementation_gap_build
md5sum INFRASTRUCTURE_INDEX.md > /tmp/after.md5
diff /tmp/before.md5 /tmp/after.md5  # expect empty diff
```
