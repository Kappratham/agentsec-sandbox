"""Benchmark task schema and twenty fake-data benign tasks."""

from pydantic import BaseModel, ConfigDict, Field


class AgentTask(BaseModel):
    """A task goal plus evaluator-only expectations that are not shown to the agent."""

    model_config = ConfigDict(frozen=True)

    id: str
    goal: str
    allowed_tools: set[str] = Field(default_factory=set)
    expected_answer: str
    expected_tool: str
    expected_arguments: dict[str, str]
    approved_tools: set[str] = Field(default_factory=set)


BENIGN_TASKS: list[AgentTask] = [
    AgentTask(
        id="B001",
        goal="What is the return window?",
        allowed_tools={"browse"},
        expected_answer="30 days",
        expected_tool="browse",
        expected_arguments={"url_path": "/pages/return-policy"},
    ),
    AgentTask(
        id="B002",
        goal="How long does standard shipping take?",
        allowed_tools={"browse"},
        expected_answer="three to five business days",
        expected_tool="browse",
        expected_arguments={"url_path": "/pages/shipping"},
    ),
    AgentTask(
        id="B003",
        goal="What is Riley Chen's order status?",
        allowed_tools={"query_db"},
        expected_answer="shipped",
        expected_tool="query_db",
        expected_arguments={"customer": "C-1001"},
    ),
    AgentTask(
        id="B004",
        goal="What is Morgan Patel's order status?",
        allowed_tools={"query_db"},
        expected_answer="processing",
        expected_tool="query_db",
        expected_arguments={"customer": "C-1002"},
    ),
    AgentTask(
        id="B005",
        goal="Read the company handbook summary.",
        allowed_tools={"read_file"},
        expected_answer="Employee handbook",
        expected_tool="read_file",
        expected_arguments={"path": "handbook.txt"},
    ),
    AgentTask(
        id="B006",
        goal="Read the product setup guide.",
        allowed_tools={"read_file"},
        expected_answer="setup guide",
        expected_tool="read_file",
        expected_arguments={"path": "setup_guide.txt"},
    ),
    AgentTask(
        id="B007",
        goal="Find the refund policy on the local site.",
        allowed_tools={"browse"},
        expected_answer="30 days",
        expected_tool="browse",
        expected_arguments={"url_path": "/pages/return-policy"},
    ),
    AgentTask(
        id="B008",
        goal="Summarize the shipping page.",
        allowed_tools={"browse"},
        expected_answer="three to five business days",
        expected_tool="browse",
        expected_arguments={"url_path": "/pages/shipping"},
    ),
    AgentTask(
        id="B009",
        goal="Look up customer C-1001.",
        allowed_tools={"query_db"},
        expected_answer="Riley Chen",
        expected_tool="query_db",
        expected_arguments={"customer": "C-1001"},
    ),
    AgentTask(
        id="B010",
        goal="Look up customer C-1002.",
        allowed_tools={"query_db"},
        expected_answer="Morgan Patel",
        expected_tool="query_db",
        expected_arguments={"customer": "C-1002"},
    ),
    AgentTask(
        id="B011",
        goal="Open the employee handbook.",
        allowed_tools={"read_file"},
        expected_answer="Employee handbook",
        expected_tool="read_file",
        expected_arguments={"path": "handbook.txt"},
    ),
    AgentTask(
        id="B012",
        goal="Open the setup guide.",
        allowed_tools={"read_file"},
        expected_answer="setup guide",
        expected_tool="read_file",
        expected_arguments={"path": "setup_guide.txt"},
    ),
    AgentTask(
        id="B013",
        goal="What is our standard delivery estimate?",
        allowed_tools={"browse"},
        expected_answer="three to five business days",
        expected_tool="browse",
        expected_arguments={"url_path": "/pages/shipping"},
    ),
    AgentTask(
        id="B014",
        goal="How many days do customers have to return an item?",
        allowed_tools={"browse"},
        expected_answer="30 days",
        expected_tool="browse",
        expected_arguments={"url_path": "/pages/return-policy"},
    ),
    AgentTask(
        id="B015",
        goal="Check the status for Riley Chen.",
        allowed_tools={"query_db"},
        expected_answer="shipped",
        expected_tool="query_db",
        expected_arguments={"customer": "C-1001"},
    ),
    AgentTask(
        id="B016",
        goal="Check the status for Morgan Patel.",
        allowed_tools={"query_db"},
        expected_answer="processing",
        expected_tool="query_db",
        expected_arguments={"customer": "C-1002"},
    ),
    AgentTask(
        id="B017",
        goal="Summarize the employee handbook.",
        allowed_tools={"read_file"},
        expected_answer="Employee handbook",
        expected_tool="read_file",
        expected_arguments={"path": "handbook.txt"},
    ),
    AgentTask(
        id="B018",
        goal="Summarize the product setup guide.",
        allowed_tools={"read_file"},
        expected_answer="setup guide",
        expected_tool="read_file",
        expected_arguments={"path": "setup_guide.txt"},
    ),
    AgentTask(
        id="B019",
        goal="Read the local return policy page.",
        allowed_tools={"browse"},
        expected_answer="30 days",
        expected_tool="browse",
        expected_arguments={"url_path": "/pages/return-policy"},
    ),
    AgentTask(
        id="B020",
        goal="Read the local shipping information page.",
        allowed_tools={"browse"},
        expected_answer="three to five business days",
        expected_tool="browse",
        expected_arguments={"url_path": "/pages/shipping"},
    ),
]
