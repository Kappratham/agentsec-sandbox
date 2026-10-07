"""Structured and serializable agent traces."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class TraceEvent(BaseModel):
    """One timestamped event in an agent run."""

    sequence: int
    event_type: Literal[
        "llm_call",
        "tool_call",
        "tool_result",
        "final",
        "attack_injection",
        "defense_block",
        "context_isolation",
    ]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    elapsed_ms: float = 0.0
    data: dict[str, Any] = Field(default_factory=dict)


class AgentTrace(BaseModel):
    """Complete trace for one task; JSON round-trips preserve every model/tool event."""

    task_id: str
    model: str
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    finished_at: datetime | None = None
    events: list[TraceEvent] = Field(default_factory=list)
    final_answer: str = ""

    def add_event(
        self,
        event_type: Literal[
            "llm_call",
            "tool_call",
            "tool_result",
            "final",
            "attack_injection",
            "defense_block",
            "context_isolation",
        ],
        data: dict[str, Any],
        elapsed_ms: float = 0.0,
    ) -> None:
        """Append an event with a monotonic sequence number."""

        self.events.append(
            TraceEvent(
                sequence=len(self.events),
                event_type=event_type,
                data=data,
                elapsed_ms=elapsed_ms,
            )
        )

    def to_json(self) -> str:
        """Serialize the complete trace for storage or replay."""

        return self.model_dump_json(indent=2)

    @classmethod
    def from_json(cls, value: str) -> AgentTrace:
        """Restore a trace from its serialized representation."""

        return cls.model_validate_json(value)

    def replay_tool_results(self) -> list[tuple[str, dict[str, Any]]]:
        """Return recorded tool result pairs without re-executing any tools."""

        call_ids: list[str] = []
        results: list[tuple[str, dict[str, Any]]] = []
        for event in self.events:
            if event.event_type == "tool_call":
                call_ids.append(str(event.data["call_id"]))
            elif event.event_type == "tool_result":
                if not call_ids:
                    raise ValueError("trace has a tool result without a preceding tool call")
                results.append((call_ids.pop(0), event.data))
        if call_ids:
            raise ValueError("trace has a tool call without a recorded result")
        return results
