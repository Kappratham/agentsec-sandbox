import json
from pathlib import Path

from agentsec.attacks.library import load_base_attacks
from agentsec.defenses.config import ablation_stacks
from agentsec.evaluators.deterministic import EvaluationStatus
from agentsec.report.analysis import generate_report, wilson_interval
from agentsec.runner.database import ResultsDatabase
from agentsec.runner.models import RunRecord, TrialRecord


def test_wilson_interval_handles_empty_and_small_samples() -> None:
    assert wilson_interval(0, 0) is None
    interval = wilson_interval(2, 2)
    assert interval is not None
    assert interval[0] < 0.5 < interval[1]
    assert interval[1] == 1.0


def test_ablation_plan_has_baseline_singles_and_cumulative_stacks() -> None:
    stacks = ablation_stacks()
    assert len(stacks) == 12
    assert stacks[0] == ["D0"]
    assert stacks[1:7] == [[f"D{i}"] for i in range(1, 7)]
    assert stacks[-1] == [f"D{i}" for i in range(1, 7)]


def test_report_uses_saved_trials_and_writes_svg(tmp_path: Path) -> None:
    database_path = tmp_path / "results.sqlite3"
    database = ResultsDatabase(database_path)
    attack = load_base_attacks()[0]
    run = RunRecord(
        evaluation_type="attack",
        backend="fixture",
        model="fixture-model",
        seed=42,
        defenses=["D0"],
        requested_trials=2,
        attack_count=1,
    )
    database.add_run(run)
    for index, status in enumerate([EvaluationStatus.FAIL, EvaluationStatus.PASS]):
        database.add_trial(
            TrialRecord(
                run_id=run.id,
                evaluation_type="attack",
                task_id="B003",
                attack_id=attack.id,
                category=attack.category.value,
                mutation_type=attack.mutation_type.value,
                trial_index=index,
                status=status,
                reasoning="fixture result",
                trace_json=json.dumps({"events": []}),
                elapsed_seconds=1.0,
                prompt_tokens=10,
                completion_tokens=5,
            )
        )

    report_path = tmp_path / "REPORT.md"
    result = generate_report([database_path], report_path)

    assert result == {"runs": 1, "trials": 2, "attack_ids": 1}
    report = report_path.read_text(encoding="utf-8")
    assert "50.0%" in report
    assert "Wilson 95% CI" in report
    assert "No benign utility" in report
    assert (tmp_path / "results" / "asr_by_defense.svg").exists()
