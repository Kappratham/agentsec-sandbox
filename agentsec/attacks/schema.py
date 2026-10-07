"""Pydantic attack-library schema and machine-checkable success criteria."""

from __future__ import annotations

import re
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AttackCategory(StrEnum):
    """Attack categories supported by the initial corpus."""

    DIRECT_PROMPT_INJECTION = "direct_prompt_injection"
    INDIRECT_WEBPAGE = "indirect_webpage"
    INDIRECT_DOCUMENT = "indirect_document"
    MALICIOUS_TOOL_OUTPUT = "malicious_tool_output"
    TOOL_POISONING = "tool_poisoning"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    DATA_EXFILTRATION = "data_exfiltration"
    MEMORY_POISONING = "memory_poisoning"


class AttackChannel(StrEnum):
    """Untrusted source through which attack content enters the target agent."""

    USER_INPUT = "user_input"
    WEBPAGE = "webpage"
    DOCUMENT = "document"
    TOOL_OUTPUT = "tool_output"
    MEMORY = "memory"
    TOOL_DESCRIPTION = "tool_description"


class OWASPRisk(StrEnum):
    """Risk labels from the OWASP GenAI LLM Top 10 2026 edition."""

    LLM01 = "LLM01:2026 Prompt Injection"
    LLM02 = "LLM02:2026 Sensitive Information Disclosure"
    LLM03 = "LLM03:2026 Excessive Agency"
    LLM04 = "LLM04:2026 Supply Chain"
    LLM05 = "LLM05:2026 Data and Model Poisoning"
    LLM06 = "LLM06:2026 Unbounded Consumption"
    LLM07 = "LLM07:2026 Misinformation"
    LLM08 = "LLM08:2026 Hidden Context Exposure"
    LLM09 = "LLM09:2026 Vector and Embedding Weaknesses"
    LLM10 = "LLM10:2026 Improper Output Handling"


class NISTRiskArea(StrEnum):
    """Applicable risk areas named in the NIST AI RMF Generative AI Profile."""

    INFORMATION_SECURITY = "NIST AI RMF GenAI Profile: Information Security"
    DATA_PRIVACY = "NIST AI RMF GenAI Profile: Data Privacy"
    HUMAN_AI_CONFIGURATION = "NIST AI RMF GenAI Profile: Human-AI Configuration"
    INFORMATION_INTEGRITY = "NIST AI RMF GenAI Profile: Information Integrity"
    VALUE_CHAIN = "NIST AI RMF GenAI Profile: Value Chain and Component Integration"


class MutationType(StrEnum):
    """Stable mutation labels for filtering reports by transformation."""

    BASE = "base"
    PARAPHRASE = "paraphrase"
    INSTRUCTION_HIDING = "instruction_hiding"
    ENCODING_BASE64 = "encoding_base64"
    ENCODING_ROT13 = "encoding_rot13"
    LANGUAGE_SWITCH = "language_switch"
    ROLE_PLAY = "role_play"
    DELIMITER_CONFUSION = "delimiter_confusion"
    PAYLOAD_SPLITTING = "payload_splitting"


class CriterionOperator(StrEnum):
    """Comparison operators supported by the deterministic evaluator."""

    EQUALS = "equals"
    CONTAINS = "contains"
    REGEX = "regex"
    EXISTS = "exists"


class TraceEventType(StrEnum):
    """Trace locations that can satisfy an attack success condition."""

    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    FINAL = "final"


class MachineCriterion(BaseModel):
    """Safe path lookup and comparison, with no executable expressions."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    event_type: TraceEventType
    field: str = Field(min_length=1)
    operator: CriterionOperator
    value: str = ""

    @field_validator("field")
    @classmethod
    def path_must_be_simple(cls, value: str) -> str:
        if not re.fullmatch(r"[A-Za-z0-9_.]+", value):
            raise ValueError("criterion field must be a simple dotted path")
        return value

    def matches(self, event: dict[str, Any]) -> bool:
        """Return whether a trace event satisfies this declared criterion."""

        if event.get("event_type") != self.event_type.value:
            return False
        current: Any = event.get("data", {})
        for part in self.field.split("."):
            if not isinstance(current, dict) or part not in current:
                return self.operator == CriterionOperator.EXISTS and False
            current = current[part]
        if self.operator == CriterionOperator.EXISTS:
            return True
        actual = str(current)
        if self.operator == CriterionOperator.EQUALS:
            return actual == self.value
        if self.operator == CriterionOperator.CONTAINS:
            return self.value in actual
        if self.operator == CriterionOperator.REGEX:
            return re.search(self.value, actual) is not None
        return False


class PayloadFragment(BaseModel):
    """One piece of a payload split across independent untrusted sources."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    channel: AttackChannel
    payload: str = Field(min_length=1)
    order: int = Field(ge=0)


class AttackRecord(BaseModel):
    """Fully expanded attack record consumed by the runner and evaluator."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str = Field(pattern=r"^[A-Z0-9][A-Z0-9_-]{2,100}$")
    category: AttackCategory
    name: str = Field(min_length=3, max_length=160)
    description: str = Field(min_length=8, max_length=500)
    channel: AttackChannel
    payload: str = Field(min_length=1)
    target_tool: str = Field(min_length=2, max_length=64)
    success_criteria: list[MachineCriterion] = Field(min_length=1)
    severity: Literal["low", "med", "high", "critical"]
    mapped_owasp: list[OWASPRisk] = Field(min_length=1)
    mapped_nist: list[NISTRiskArea] = Field(min_length=1)
    base_attack_id: str | None = None
    mutation_type: MutationType = MutationType.BASE
    payload_fragments: list[PayloadFragment] = Field(default_factory=list)


class AttackDefinition(BaseModel):
    """Compact source definition; category-level metadata is added during loading."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str
    name: str
    description: str
    payload: str


class CategoryDefinition(BaseModel):
    """Defaults shared by the attack records in one category."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    category: AttackCategory
    channel: AttackChannel
    target_tool: str
    severity: Literal["low", "med", "high", "critical"]
    mapped_owasp: list[OWASPRisk] = Field(min_length=1)
    mapped_nist: list[NISTRiskArea] = Field(min_length=1)
    attacks: list[AttackDefinition] = Field(min_length=10)


class AttackLibrarySource(BaseModel):
    """Top-level source format for the checked-in base corpus."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal[1]
    categories: list[CategoryDefinition] = Field(min_length=8)
