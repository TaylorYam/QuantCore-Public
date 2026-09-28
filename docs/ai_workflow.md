# AI-assisted engineering workflow

Claude Code and Codex assist implementation, refactoring, debugging, test generation, documentation, research tooling and repetitive engineering tasks. The developer supplies the problem, domain model and acceptance criteria, reviews evidence and owns the final decision.

1. Open an issue with observable behavior, synthetic reproduction and acceptance criteria.
2. Create a feature branch in an isolated worktree, using the actual issue number:

   ```sh
   git worktree add ../quantcore-task -b feat/example-task main
   ```

   This example assumes an initialized main branch. Worktrees isolate code, not external state; use temporary output directories and synthetic fixtures.
3. Implement and review small changes. For refactors, record deterministic before/after outputs. For research changes, record data provenance, assumptions and all validation outcomes.
4. Run offline tests, demo and public-content checks. Review the diff for sensitive information and unsupported claims.
5. Open a PR linked to the issue; explain behavior, limitations and exact validation results.
6. Require CI and human review before merging. Configure branch protection when creating the hosted repository.

Human control covers trading logic, architecture decisions, validation standards, risk management and publication. AI agents never modify live configuration or execute live trading in this public project. Data-backed strategy decisions require separate research review; passing software tests does not validate profitability.

Issue and PR templates are provided as workflow scaffolding, not fabricated historical evidence. ADRs record this demonstration's design choices. No private issue history or internal research decisions are imported.
