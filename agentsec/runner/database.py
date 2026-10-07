"""SQLite storage for experiment run metadata and trial traces."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from agentsec.runner.models import RunRecord, TrialRecord


class ResultsDatabase:
    """Small local SQLite repository with no networked database dependencies."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS runs ("
                "id TEXT PRIMARY KEY, created_at TEXT NOT NULL, evaluation_type TEXT NOT NULL, "
                "backend TEXT NOT NULL, model TEXT NOT NULL, temperature REAL NOT NULL, "
                "seed INTEGER, defenses_json TEXT NOT NULL, requested_trials INTEGER NOT NULL, "
                "attack_count INTEGER NOT NULL, task_count INTEGER NOT NULL)"
            )
            connection.execute(
                "CREATE TABLE IF NOT EXISTS trial_results ("
                "id TEXT PRIMARY KEY, run_id TEXT NOT NULL REFERENCES runs(id), "
                "evaluation_type TEXT NOT NULL, task_id TEXT NOT NULL, attack_id TEXT, "
                "category TEXT, mutation_type TEXT, trial_index INTEGER NOT NULL, "
                "status TEXT NOT NULL, reasoning TEXT NOT NULL, trace_json TEXT NOT NULL, "
                "elapsed_seconds REAL NOT NULL, prompt_tokens INTEGER NOT NULL, "
                "completion_tokens INTEGER NOT NULL, created_at TEXT NOT NULL)"
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_trial_results_run ON trial_results(run_id)"
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_trial_results_attack ON trial_results(attack_id)"
            )

    def add_run(self, run: RunRecord) -> None:
        """Persist batch metadata."""

        with self._connect() as connection:
            connection.execute(
                "INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    run.id,
                    run.created_at.isoformat(),
                    run.evaluation_type,
                    run.backend,
                    run.model,
                    run.temperature,
                    run.seed,
                    json.dumps(run.defenses),
                    run.requested_trials,
                    run.attack_count,
                    run.task_count,
                ),
            )

    def add_trial(self, trial: TrialRecord) -> None:
        """Persist a result and trace immediately so interrupted batches retain completed work."""

        with self._connect() as connection:
            connection.execute(
                "INSERT INTO trial_results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    trial.id,
                    trial.run_id,
                    trial.evaluation_type,
                    trial.task_id,
                    trial.attack_id,
                    trial.category,
                    trial.mutation_type,
                    trial.trial_index,
                    trial.status.value,
                    trial.reasoning,
                    trial.trace_json,
                    trial.elapsed_seconds,
                    trial.prompt_tokens,
                    trial.completion_tokens,
                    trial.created_at.isoformat(),
                ),
            )

    def trial_count(self, run_id: str | None = None) -> int:
        """Count stored trial rows."""

        with self._connect() as connection:
            if run_id is None:
                row = connection.execute("SELECT COUNT(*) AS count FROM trial_results").fetchone()
            else:
                row = connection.execute(
                    "SELECT COUNT(*) AS count FROM trial_results WHERE run_id = ?", (run_id,)
                ).fetchone()
        return int(row["count"])

    def completed_trial_keys(
        self,
        *,
        evaluation_type: str,
        backend: str,
        model: str,
        temperature: float,
        seed: int | None,
        defenses: list[str],
    ) -> set[tuple[str, int]]:
        """Return successful or failed trial keys for an identical run configuration."""

        with self._connect() as connection:
            rows = connection.execute(
                "SELECT t.attack_id,t.task_id,t.trial_index FROM trial_results t "
                "JOIN runs r ON t.run_id=r.id WHERE r.evaluation_type=? AND r.backend=? "
                "AND r.model=? AND r.temperature=? AND r.seed IS ? AND r.defenses_json=? "
                "AND t.status IN ('PASS','FAIL')",
                (
                    evaluation_type,
                    backend,
                    model,
                    temperature,
                    seed,
                    json.dumps(defenses),
                ),
            ).fetchall()
        return {(str(row["attack_id"] or row["task_id"]), int(row["trial_index"])) for row in rows}

    def trials_for_run(self, run_id: str) -> list[TrialRecord]:
        """Return all persisted trial records for one batch."""

        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM trial_results WHERE run_id = ? ORDER BY created_at, trial_index",
                (run_id,),
            ).fetchall()
        return [TrialRecord.model_validate(dict(row)) for row in rows]
