"""Defense identifiers and validation."""

from enum import StrEnum


class DefenseID(StrEnum):
    """Independently selectable benchmark defenses."""

    BASELINE = "D0"
    HARDENED_PROMPT = "D1"
    TOOL_ALLOWLIST = "D2"
    UNTRUSTED_SPOTLIGHT = "D3"
    EGRESS_VALIDATION = "D4"
    CONTEXT_ISOLATION = "D5"
    HUMAN_CONFIRMATION = "D6"


def normalize_defenses(defenses: list[str] | None) -> list[str]:
    """Validate and normalize a baseline or defense-stack selection."""

    values = defenses or [DefenseID.BASELINE.value]
    normalized = list(dict.fromkeys(value.strip().upper() for value in values))
    allowed = {defense.value for defense in DefenseID}
    unknown = sorted(set(normalized) - allowed)
    if unknown:
        raise ValueError(f"unknown defense IDs: {', '.join(unknown)}")
    if DefenseID.BASELINE.value in normalized and len(normalized) > 1:
        raise ValueError("D0 baseline cannot be combined with other defenses")
    return normalized


def ablation_stacks() -> list[list[str]]:
    """Return baseline, independent layers, then cumulative D1-to-D6 stacks."""

    layers = [defense.value for defense in list(DefenseID)[1:]]
    stacks = [[DefenseID.BASELINE.value], *[[layer] for layer in layers]]
    stacks.extend([layers[:count] for count in range(2, len(layers) + 1)])
    return stacks
