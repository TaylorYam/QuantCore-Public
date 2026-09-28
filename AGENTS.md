# Agent collaboration rules

Read `CONTEXT.md` and `docs/adr/README.md` before changing interfaces. Read `docs/validation.md` when modifying research tools.

- Work from one issue on one branch and one isolated worktree; keep a single writer per branch. Follow the workflow in `docs/ai_workflow.md`.
- Use synthetic inputs and mock execution only. Never add broker connections, credential loading, live execution, notification delivery or private source files.
- Keep Strategy independent of Account and execution. Preserve chronological train/test separation and validate data before evaluation.
- Strategy claims require reproducible evidence and human review. Artificial example output is not investment performance.
- For behavior-preserving refactors, capture deterministic outputs before editing and compare them afterward. Use temporary directories for generated artifacts.
- Before requesting review, run the checks in README, update relevant docs and inspect every added file for sensitive content.
- Record architecture changes in an ADR. New ADRs describe this public demonstration only.
- Merge requires passing CI and human approval. Publishing requires explicit owner approval of the final privacy review.
