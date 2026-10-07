"""Agreement metrics for comparing optional judge labels with human labels."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

CalibrationLabel = Literal["PASS", "FAIL"]


class CalibrationRow(BaseModel):
    """Paired human and judge labels for one trace."""

    trace_id: str = Field(min_length=1)
    human_label: CalibrationLabel
    judge_label: CalibrationLabel


class CalibrationReport(BaseModel):
    """Exact agreement, Cohen's kappa, and disagreements for paired labels."""

    sample_count: int
    agreement_count: int
    agreement_rate: float
    cohen_kappa: float | None
    disagreement_trace_ids: list[str]
    warning: str | None = None


def load_calibration_csv(path: Path) -> list[CalibrationRow]:
    """Load paired labels from CSV columns trace_id,human_label,judge_label."""

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required = {"trace_id", "human_label", "judge_label"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("CSV must include trace_id, human_label, and judge_label columns")
        rows = [CalibrationRow.model_validate(row) for row in reader]
    if not rows:
        raise ValueError("calibration CSV has no labeled traces")
    ids = [row.trace_id for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("calibration CSV contains duplicate trace IDs")
    return rows


def compute_calibration(rows: list[CalibrationRow]) -> CalibrationReport:
    """Compute exact agreement and Cohen's kappa for binary labels."""

    if not rows:
        raise ValueError("at least one paired label is required")
    agreement_count = sum(row.human_label == row.judge_label for row in rows)
    agreement_rate = agreement_count / len(rows)
    human_pass = sum(row.human_label == "PASS" for row in rows) / len(rows)
    judge_pass = sum(row.judge_label == "PASS" for row in rows) / len(rows)
    expected_agreement = human_pass * judge_pass + (1 - human_pass) * (1 - judge_pass)
    kappa = (
        (agreement_rate - expected_agreement) / (1 - expected_agreement)
        if expected_agreement < 1
        else None
    )
    return CalibrationReport(
        sample_count=len(rows),
        agreement_count=agreement_count,
        agreement_rate=agreement_rate,
        cohen_kappa=kappa,
        disagreement_trace_ids=[row.trace_id for row in rows if row.human_label != row.judge_label],
        warning=(
            "Fewer than 30 paired labels; treat agreement as preliminary."
            if len(rows) < 30
            else None
        ),
    )
