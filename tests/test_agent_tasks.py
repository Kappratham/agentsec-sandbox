from pathlib import Path

from agentsec.agent.react import ReActAgent
from agentsec.agent.tasks import BENIGN_TASKS
from agentsec.agent.trace import AgentTrace
from agentsec.env.tools import MockEnvironment
from agentsec.env.web import MockWebServer
from agentsec.llm.testing import TaskFixtureBackend


def test_all_twenty_benign_tasks_complete_and_traces_replay(tmp_path: Path) -> None:
    web = MockWebServer()
    env = MockEnvironment(
        sandbox_dir=Path("data/sandbox").resolve(),
        database_path=tmp_path / "customers.sqlite3",
        web=web,
    )
    with env:
        backend = TaskFixtureBackend(BENIGN_TASKS, web.base_url)
        agent = ReActAgent(backend=backend, environment=env)
        completed = 0
        for task in BENIGN_TASKS:
            result = agent.run(task, use_cache=False)
            assert task.expected_answer.casefold() in result.answer.casefold()
            assert [event.event_type for event in result.trace.events].count("llm_call") == 2
            assert [event.event_type for event in result.trace.events].count("tool_call") == 1
            assert [event.event_type for event in result.trace.events].count("tool_result") == 1
            restored = AgentTrace.from_json(result.trace.to_json())
            replayed = restored.replay_tool_results()
            assert len(replayed) == 1
            assert replayed[0][0] == f"fixture-{task.id}"
            completed += 1

    assert completed == 20
