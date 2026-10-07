from pathlib import Path

import pytest

from agentsec.env.tools import MockEnvironment, ToolError
from agentsec.env.web import MockWebServer


@pytest.fixture
def environment(tmp_path: Path):
    sandbox = tmp_path / "sandbox"
    sandbox.mkdir()
    (sandbox / "safe.txt").write_text("safe fixture", encoding="utf-8")
    (sandbox / ".env").write_text("FAKE_KEY=CANARY-0000", encoding="utf-8")
    outside = tmp_path / "outside.txt"
    outside.write_text("outside", encoding="utf-8")
    env = MockEnvironment(
        sandbox_dir=sandbox,
        database_path=tmp_path / "customers.sqlite3",
        web=MockWebServer(),
    )
    env.start()
    env.outside_test_path = outside  # type: ignore[attr-defined]
    yield env
    env.close()


@pytest.mark.parametrize(
    "path",
    [
        "C:\\Windows\\win.ini",
        "C:/Windows/win.ini",
        "/etc/passwd",
        "..\\outside.txt",
        "../outside.txt",
        ".env",
        "sub\\..\\.env",
        "http://example.com/secret",
        "safe.txt:stream",
    ],
)
def test_read_file_rejects_paths_outside_sandbox(environment: MockEnvironment, path: str) -> None:
    with pytest.raises(ToolError):
        environment.read_file(path)


def test_read_file_accepts_a_fixture(environment: MockEnvironment) -> None:
    assert environment.read_file("safe.txt").content == "safe fixture"


def test_read_file_rejects_absolute_path_to_existing_outside_file(
    environment: MockEnvironment,
) -> None:
    outside = environment.outside_test_path  # type: ignore[attr-defined]
    with pytest.raises(ToolError):
        environment.read_file(str(outside))


def test_read_file_rejects_symlink_escape(environment: MockEnvironment, tmp_path: Path) -> None:
    link = environment.sandbox_dir / "escape.txt"
    try:
        link.symlink_to(tmp_path / "outside.txt")
    except (OSError, NotImplementedError):
        pytest.skip("Windows symlink creation is not available for this account")
    with pytest.raises(ToolError):
        environment.read_file("escape.txt")


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com/",
        "http://127.0.0.1:1/",
        "file:///C:/Users/secret/.env",
        "http://localhost:80/../../.env",
    ],
)
def test_browse_rejects_non_mock_urls_and_traversal(environment: MockEnvironment, url: str) -> None:
    with pytest.raises(ToolError):
        environment.browse(url)


def test_browse_reads_only_mock_server_page(environment: MockEnvironment) -> None:
    page = environment.browse(environment.web.url_for("/pages/shipping"))
    assert "three to five business days" in page.content


def test_query_db_reads_fake_rows(environment: MockEnvironment) -> None:
    result = environment.query_db(
        "SELECT name, order_status FROM customers WHERE customer_id = 'C-1001'"
    )
    assert result.data == [{"name": "Riley Chen", "order_status": "shipped"}]


@pytest.mark.parametrize(
    "sql",
    [
        "DELETE FROM customers",
        "ATTACH DATABASE 'C:/Users/secret/.env' AS x",
        "SELECT * FROM customers; DROP TABLE customers",
        "SELECT load_extension('x')",
        "SELECT readfile('../.env')",
        "SELECT 'https://example.com'",
    ],
)
def test_query_db_rejects_writes_files_and_external_references(
    environment: MockEnvironment, sql: str
) -> None:
    with pytest.raises(ToolError):
        environment.query_db(sql)


def test_send_email_writes_only_to_local_outbox(environment: MockEnvironment) -> None:
    environment.send_email("test@example.test", "Hello", "Local test")
    assert len(environment.outbox) == 1
    with pytest.raises(ToolError):
        environment.send_email("https://example.com", "Hello", "No delivery")
    with pytest.raises(ToolError):
        environment.send_email("C:\\Users\\secret\\.env", "Hello", "No file access")


def test_memory_keys_cannot_be_paths_or_env_files(environment: MockEnvironment) -> None:
    environment.memory_write("task-note", "Local note")
    assert environment.memory_read("task-note").content == "Local note"
    for key in ("C:\\Users\\secret\\.env", "../.env", ".env", "https://example.com"):
        with pytest.raises(ToolError):
            environment.memory_write(key, "blocked")
