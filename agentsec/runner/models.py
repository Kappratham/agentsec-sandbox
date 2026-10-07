"""Validated run and trial records persisted in SQLite."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field

from agentsec.evaluators.deterministic import EvaluationStatus


class RunRecord(BaseModel):
    """Metadata describing one reproducible batch."""

    id: str = Field(default_factory=lambda: uuid4().hex)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    evaluation_type: Literal["attack", "benign"]
    backend: str
    model: str
    temperature: float = 0.0
    seed: int | None = None
    defenses: list[str] = Field(default_factory=lambda: ["D0"])
    requested_trials: int = Field(ge=1)
    attack_count: int = 0
    task_count: int = 0


class TrialRecord(BaseModel):
    """One individual trial result with its complete trace."""

    id: str = Field(default_factory=lambda: uuid4().hex)
    run_id: str
    evaluation_type: Literal["attack", "benign"]
    task_id: str
    attack_id: str | None = None
    category: str | None = None
    mutation_type: str | None = None
    trial_index: int = Field(ge=0)
    status: EvaluationStatus
    reasoning: str
    trace_json: str
    elapsed_seconds: float = Field(ge=0)
    prompt_tokens: int = Field(ge=0)
    completion_tokens: int = Field(ge=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
