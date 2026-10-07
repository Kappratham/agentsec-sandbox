# AgentSec Sandbox

AgentSec Sandbox is a reproducible, local framework for measuring prompt-injection and tool-abuse attacks against an intentionally vulnerable tool-using agent. It uses fake data, local mock tools, and canary secrets.

## Windows setup (PowerShell)

1. Install Python 3.11 or newer.
2. Open PowerShell in this folder.
3. Create an environment: `py -3.11 -m venv .venv`.
4. Activate it: `.\.venv\Scripts\Activate.ps1`.
5. Install the project: `python -m pip install -e ".[dev]"`.
6. Copy settings template: `Copy-Item .env.example .env`.
7. Add your Groq key to `.env` on your machine, or set `LLM_BACKEND=ollama` after installing and starting Ollama locally.
8. Run `agentsec doctor` to check the selected backend and tests.

The Groq API key is read by the host process and is not included in prompts, tools, or traces. Agent tools will use in-process restrictions and the local mock environment; they do not make model calls.

## Development

- `python tasks.py test` runs the test suite.
- `python tasks.py lint` runs Ruff.
- `python tasks.py doctor` checks the configured model backend and tests.
- `agentsec run --defenses D0 --trials 5 --seed 42 --attack-id DIR001` runs selected measured attack trials after a backend is configured. Select a defense stack with comma-separated IDs, such as `--defenses D1,D2,D4`. Use `--suite benign` for the benign task suite. `agentsec calibrate-judge --labels labels.csv` computes agreement from paired human and judge labels.
- `agentsec reproduce` runs the full attack and benign ablation with independent and cumulative defense stacks, resumes completed trials, and regenerates `REPORT.md`. Use `--max-attacks 8 --trials 1 --skip-benign` for a smaller pilot. `agentsec report` regenerates the report from saved SQLite files without making model calls.

## Phase 1 sandbox

The baseline agent is a small host-side ReAct loop. Its tools use fake documents and a fake SQLite customer database, browse a page map served on loopback, save mail only to an in-memory mock outbox, and keep notes in local in-process memory. The browse tool accepts only the active mock server origin. File reads reject absolute paths, traversal, `.env`, and symlink escapes. Database queries use a read-only connection and accept one `SELECT` statement.

Run `agentsec doctor` after configuring a backend. It checks for a missing Groq key, probes the selected model, then runs the full test suite, including sandbox boundary checks. The deterministic offline fixture backend is used by tests to exercise 20 benign tasks without contacting a model provider.

## Attack corpus

Run `agentsec attacks validate` to validate and expand the checked-in corpus. It contains 80 base attacks across eight categories; deterministic mutations expand those to 640 records. Optional paraphrasing is available through the configured backend, but the default validation command makes no model calls.

## Defense layers

- D0: vulnerable baseline with no defenses.
- D1: hardened system prompt that identifies external content as data.
- D2: task-specific tool allowlist enforced in both tool schemas and execution.
- D3: labels and sanitizes untrusted text, then quotes it as data.
- D4: blocks canary-bearing email arguments and recipients outside the safe allowlist.
- D5: sends untrusted text to a tool-free extraction call and passes only validated JSON fields to the agent.
- D6: simulated confirmation gate for email; calls are denied unless that task explicitly carries an approval.

Stack defenses with comma-separated IDs, for example `agentsec run --defenses D1,D2,D4 --trials 5`. D0 is selected alone. D5 adds model calls and latency; its parser fails closed when isolated output is not valid structured data.

## Project structure

`agentsec/` contains the Python package. `tests/` contains checks. `data/`, `attack_library/`, `configs/`, and experiment outputs under `results/` contain the sandbox, attack corpus, and local SQLite results. Local `.env` and full result files are ignored by Git.

## Status

Phases 0–5 tooling is in place. The current Ollama benchmark is a resumable partial run: saved results cover 29 of 640 expanded attack IDs, with coverage varying across the 12 defense configurations. The report documents the measured results and limitations. Full attack and benign utility coverage under every defense, plus judge calibration with human-labeled data, remain pending.
