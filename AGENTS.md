# 📖 KodaWiki Agent Schema & Guidelines (AGENTS.md)

This schema document instructs KodaWiki Multi-Agent System on maintaining the living knowledge base and following project coding standards.

---

## 🗂️ 1. Living Wiki Structure (`.kodawiki/`)

- `.kodawiki/index.md`: Catalog of all components, API routes, data models, and test modules.
- `.kodawiki/log.md`: Chronological append-only record of all agent operations.
- `.kodawiki/modules/`: Component-specific architectural documentation.

---

## 🤖 2. Agent Execution Rules

### Planner Agent
- MUST query `.kodawiki/index.md` before generating an execution plan.
- NEVER request modifications to files not relevant to the task scope.

### Coder Agent
- Follow clean Python code standards (PEP8, type hints, docstrings).
- Ensure all created/modified functions have corresponding unit tests.

### Tester Agent
- Run tests in isolated Sandbox (`pytest`).
- Capture both `stdout` and `stderr` for evaluation.

### Debugger Agent
- Parse tracebacks and identify precise lines causing failures.
- Limit max retry attempts to 3 iterations before asking for human intervention.

### Wiki Maintainer Agent
- Inspect `git diff` upon test completion.
- Update `.kodawiki/index.md` and append entry to `.kodawiki/log.md`.
