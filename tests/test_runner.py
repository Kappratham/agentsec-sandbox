from pathlib import Path

from agentsec.agent.tasks import BENIGN_TASKS
from agentsec.attacks.library import load_base_attacks
from agentsec.attacks.schema import AttackCategory
from agentsec.evaluators.deterministic import EvaluationStatus
from agentsec.llm.models import LLMRequest, LLMResponse, ToolCall
from agentsec.runner.core import ExperimentRunner
from agentsec.runner.database import ResultsDatabase


class OneAttackBackend:
    model = "offline-runner-fixture"

    def __init__(self) -> None:
        self.calls = 0

    def complete(self, request: LLMRequest) -> LLMResponse:
        self.calls += 1
        if self.calls == 1:
            return LLMResponse(
                model=self.model,
                tool_calls=[
                    ToolCall(
                        id="fixture-mail",
                        name="send_email",
                        arguments={
                            "to": "test@example.test",
                            "subject": "test",
                            "body": "CANARY-4F2A",
                        },
                    )
                ],
            )
        return LLMResponse(model=self.model, content="Task complete.")


class BenignAnswerBackend:
    model = "offline-benign-fixture"

    def complete(self, request: LLMRequest) -> LLMResponse:
        user_message = next(message for message in request.messages if message.role == "user")
        task = next(task for task in BENIGN_TASKS if task.goal == user_message.content)
        return LLMResponse(model=self.model, content=f"Fixture answer: {task.expected_answer}")


def test_attack_run_persists_trial_and_replayable_trace(tmp_path: Path) -> None:
    attack = next(
        attack
        for attack in load_base_attacks()
        if attack.category == AttackCategory.DATA_EXFILTRATION
    )
    database = ResultsDatabase(tmp_path / "results.sqlite3")
    runner = ExperimentRunner(backend=OneAttackBackend(), database=database)

    summary = runner.run_attacks([attack], trials=1)

    records = database.trials_for_run(summary.run_id)
    assert summary.attempted == 1
    assert summary.fail_count == 1, records[0].reasoning
    assert database.trial_count(summary.run_id) == 1
    assert records[0].status == EvaluationStatus.FAIL
    assert records[0].attack_id == attack.id
    assert records[0].trace_json.startswith("{")

    resumed = runner.run_attacks([attack], trials=1, resume=True)
    assert resumed.attempted == 0
    assert database.trial_count() == 1


def test_benign_run_records_success(tmp_path: Path) -> None:
    database = ResultsDatabase(tmp_path / "results.sqlite3")
    runner = ExperimentRunner(backend=BenignAnswerBackend(), database=database)

    summary = runner.run_benign(trials=1)

    assert summary.attempted == 20, database.trials_for_run(summary.run_id)[0].reasoning
    assert summary.pass_count == 20
    assert database.trial_count(summary.run_id) == 20
