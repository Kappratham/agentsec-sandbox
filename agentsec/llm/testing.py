"""Offline deterministic backend used only by tests and local smoke checks."""

from __future__ import annotations

from agentsec.agent.tasks import AgentTask
from agentsec.llm.models import LLMRequest, LLMResponse, ToolCall


class TaskFixtureBackend:
    """Simulate a model selecting the expected tool for each benign fixture task."""

    model = "offline-fixture-v1"

    def __init__(self, tasks: list[AgentTask], server_base_url: str) -> None:
        self._tasks = {task.goal: task for task in tasks}
        self._base_url = server_base_url

    def complete(self, request: LLMRequest) -> LLMResponse:
        user_message = next(message for message in request.messages if message.role == "user")
        task = self._tasks[user_message.content]
        tool_result = next(
            (message for message in reversed(request.messages) if message.role == "tool"), None
        )
        if tool_result is not None:
            return LLMResponse(content=f"Result: {tool_result.content}", model=self.model)

        arguments: dict[str, str]
        if task.expected_tool == "browse":
            arguments = {"url": self._base_url + task.expected_arguments["url_path"]}
        elif task.expected_tool == "query_db":
            customer = task.expected_arguments["customer"]
            arguments = {
                "sql": (
                    "SELECT customer_id, name, order_status FROM customers "
                    f"WHERE customer_id = '{customer}'"
                )
            }
        else:
            arguments = task.expected_arguments
        return LLMResponse(
            model=self.model,
            tool_calls=[
                ToolCall(id=f"fixture-{task.id}", name=task.expected_tool, arguments=arguments)
            ],
        )
