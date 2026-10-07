"""Command-line entry point."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Annotated

import typer
from openai import APIConnectionError, APIStatusError, AuthenticationError

from agentsec.attacks.library import load_attack_library, load_base_attacks
from agentsec.attacks.schema import AttackCategory
from agentsec.defenses.config import ablation_stacks, normalize_defenses
from agentsec.evaluators.calibration import compute_calibration, load_calibration_csv
from agentsec.llm.base import build_backend
from agentsec.llm.models import LLMRequest, Message
from agentsec.report.analysis import generate_report
from agentsec.runner.core import ExperimentRunner
from agentsec.runner.database import ResultsDatabase
from agentsec.settings import Settings

app = typer.Typer(no_args_is_help=True, help="Evaluate defenses for tool-using agents.")
attacks_app = typer.Typer(no_args_is_help=True, help="Inspect and validate the attack library.")
app.add_typer(attacks_app, name="attacks")


@attacks_app.command("validate")
def validate_attacks() -> None:
    """Validate attack records and report base and expanded counts."""

    base = load_base_attacks()
    expanded = load_attack_library()
    typer.echo(f"Validated {len(base)} base attacks across {len(AttackCategory)} categories.")
    typer.echo(f"Deterministically expanded library: {len(expanded)} total attacks.")


@app.command()
def run(
    defenses: Annotated[
        str,
        typer.Option("--defenses", help="Comma-separated defense stack, such as D1,D2,D4."),
    ] = "D0",
    trials: Annotated[
        int,
        typer.Option(min=1, help="Repeated trials per attack or benign task."),
    ] = 5,
    seed: Annotated[
        int,
        typer.Option(help="Master seed used to derive a stable seed for each trial."),
    ] = 42,
    attack_id: Annotated[
        list[str] | None,
        typer.Option("--attack-id", help="Select attack ID(s); defaults to the expanded corpus."),
    ] = None,
    suite: Annotated[
        str,
        typer.Option(help="Run either attacks or the benign task suite."),
    ] = "attacks",
    results_db: Annotated[
        Path,
        typer.Option(help="SQLite results path."),
    ] = Path("results") / "agentsec.sqlite3",
) -> None:
    """Run attack or benign trials and persist evaluator results and complete traces."""

    if suite not in {"attacks", "benign"}:
        typer.echo("suite must be 'attacks' or 'benign'.", err=True)
        raise typer.Exit(code=2)
    try:
        selected_defenses = normalize_defenses(defenses.split(","))
    except ValueError as error:
        typer.echo(f"Run failed: {error}.", err=True)
        raise typer.Exit(code=2) from error
    settings = Settings()
    if settings.llm_backend == "groq" and not settings.groq_api_key.get_secret_value():
        typer.echo("Run failed: GROQ_API_KEY is missing. Add it to .env on this machine.", err=True)
        raise typer.Exit(code=1)
    try:
        backend = build_backend(settings)
        runner = ExperimentRunner(
            backend=backend,
            database=ResultsDatabase(results_db),
            backend_name=settings.llm_backend,
            temperature=settings.llm_temperature,
            seed=seed,
        )
        if suite == "benign":
            summary = runner.run_benign(trials=trials, defenses=selected_defenses)
        else:
            attacks = load_attack_library()
            if attack_id:
                selected = set(attack_id)
                attacks = [attack for attack in attacks if attack.id in selected]
                if not attacks:
                    typer.echo("Run failed: no attack IDs matched.", err=True)
                    raise typer.Exit(code=2)
            summary = runner.run_attacks(attacks, trials=trials, defenses=selected_defenses)
    except typer.Exit:
        raise
    except Exception as error:
        typer.echo(f"Run failed: {type(error).__name__}.", err=True)
        raise typer.Exit(code=1) from error

    typer.echo(
        f"Run {summary.run_id}: {summary.attempted} trials; "
        f"PASS={summary.pass_count}, FAIL={summary.fail_count}, ERROR={summary.error_count}."
    )
    if suite == "attacks" and summary.pass_count + summary.fail_count:
        asr = summary.fail_count / (summary.pass_count + summary.fail_count)
        typer.echo(f"Observed ASR: {asr:.3%} (errors excluded).")
    typer.echo(f"Results saved to {results_db}.")


@app.command("calibrate-judge")
def calibrate_judge(
    labels: Annotated[
        Path,
        typer.Option(help="CSV containing trace_id, human_label, and judge_label."),
    ],
) -> None:
    """Compute agreement metrics from paired labels supplied for a judge review."""

    try:
        report = compute_calibration(load_calibration_csv(labels))
    except Exception as error:
        typer.echo(f"Calibration failed: {type(error).__name__}.", err=True)
        raise typer.Exit(code=1) from error
    typer.echo(f"Paired labels: {report.sample_count}")
    typer.echo(f"Exact agreement: {report.agreement_rate:.3%}")
    if report.cohen_kappa is None:
        typer.echo("Cohen's kappa: undefined for these label distributions.")
    else:
        typer.echo(f"Cohen's kappa: {report.cohen_kappa:.4f}")
    if report.warning:
        typer.echo(report.warning)
    if report.disagreement_trace_ids:
        typer.echo(f"Disagreements: {', '.join(report.disagreement_trace_ids)}")


@app.command()
def doctor() -> None:
    """Check provider connectivity and run the project's tests."""

    settings = Settings()
    if settings.llm_backend == "groq" and not settings.groq_api_key.get_secret_value():
        typer.echo(
            "Doctor failed: GROQ_API_KEY is missing. Add it to .env on this machine.",
            err=True,
        )
        raise typer.Exit(code=1)

    typer.echo(f"Checking {settings.llm_backend} backend ({settings.provider_model})...")
    try:
        backend = build_backend(settings)
        backend.complete(
            LLMRequest(
                messages=[Message(role="user", content="Reply with OK.")],
                temperature=0,
                use_cache=False,
            )
        )
    except (AuthenticationError, APIConnectionError, APIStatusError, OSError) as error:
        if isinstance(error, AuthenticationError):
            detail = "authentication failed; check the provider key or local backend configuration"
        elif isinstance(error, APIConnectionError):
            detail = (
                "could not connect; check your network or confirm Ollama is running on localhost"
            )
        else:
            detail = f"provider check failed ({type(error).__name__})"
        typer.echo(f"Doctor failed: {detail}.", err=True)
        raise typer.Exit(code=1) from error
    except Exception as error:
        typer.echo(f"Doctor failed: provider check failed ({type(error).__name__}).", err=True)
        raise typer.Exit(code=1) from error

    typer.echo("Backend responded successfully.")
    test_dir = Path("tests")
    if not test_dir.exists():
        typer.echo(
            "Doctor failed: tests/ is missing; boundary checks cannot be verified.",
            err=True,
        )
        raise typer.Exit(code=1)
    result = subprocess.run([sys.executable, "-m", "pytest", str(test_dir)], check=False)
    if result.returncode:
        typer.echo("Doctor failed: test suite did not pass.", err=True)
        raise typer.Exit(code=result.returncode)
    typer.echo("Test suite passed.")


@app.command()
def reproduce(
    trials: Annotated[int, typer.Option(min=1, help="Repeated trials per item/configuration.")] = 5,
    seed: Annotated[int, typer.Option(help="Master seed for paired, repeatable trials.")] = 42,
    max_attacks: Annotated[
        int | None,
        typer.Option(min=1, help="Optional attack-count cap for a smaller pilot run."),
    ] = None,
    skip_benign: Annotated[
        bool, typer.Option(help="Skip the 20-task benign utility suite.")
    ] = False,
    results_db: Annotated[
        Path, typer.Option(help="SQLite database; completed trials are resumed from this file.")
    ] = Path("results") / "agentsec.sqlite3",
) -> None:
    """Run independent and cumulative defense ablations, then regenerate REPORT.md."""

    settings = Settings()
    if settings.llm_backend == "groq" and not settings.groq_api_key.get_secret_value():
        typer.echo("Reproduction failed: GROQ_API_KEY is missing; configure it locally.", err=True)
        raise typer.Exit(code=1)
    try:
        backend = build_backend(settings)
        database = ResultsDatabase(results_db)
        runner = ExperimentRunner(
            backend=backend,
            database=database,
            backend_name=settings.llm_backend,
            temperature=settings.llm_temperature,
            seed=seed,
        )
        attacks = load_attack_library()
        if max_attacks is not None:
            attacks = attacks[:max_attacks]
        stacks = ablation_stacks()
        typer.echo(
            f"Reproduction: {len(attacks)} of {len(load_attack_library())} attacks, "
            f"{trials} trials, {len(stacks)} defense configurations."
        )
        for stack in stacks:
            label = "+".join(stack)
            typer.echo(f"Running attack suite for {label}...")
            summary = runner.run_attacks(attacks, trials=trials, defenses=stack, resume=True)
            typer.echo(
                f"  new trials={summary.attempted}, PASS={summary.pass_count}, "
                f"FAIL={summary.fail_count}, ERROR={summary.error_count}"
            )
            if not skip_benign:
                typer.echo(f"Running benign suite for {label}...")
                summary = runner.run_benign(trials=trials, defenses=stack, resume=True)
                typer.echo(
                    f"  new trials={summary.attempted}, PASS={summary.pass_count}, "
                    f"FAIL={summary.fail_count}, ERROR={summary.error_count}"
                )
        results_dir = results_db.parent
        databases = sorted(results_dir.glob("*.sqlite3"))
        report_counts = generate_report(databases, Path("REPORT.md"))
    except typer.Exit:
        raise
    except Exception as error:
        typer.echo(f"Reproduction failed: {type(error).__name__}.", err=True)
        raise typer.Exit(code=1) from error
    typer.echo(
        f"REPORT.md generated from {report_counts['runs']} runs, "
        f"{report_counts['trials']} trial rows, and {report_counts['attack_ids']} attack IDs."
    )


@app.command()
def report(
    results_dir: Annotated[
        Path, typer.Option(help="Directory containing saved results SQLite databases.")
    ] = Path("results"),
    output: Annotated[Path, typer.Option(help="Markdown report output path.")] = Path("REPORT.md"),
) -> None:
    """Regenerate the report and ASR plot from saved SQLite results only."""

    counts = generate_report(sorted(results_dir.glob("*.sqlite3")), output)
    typer.echo(
        f"Report generated from {counts['runs']} runs, {counts['trials']} trial rows, "
        f"and {counts['attack_ids']} attack IDs: {output}."
    )


if __name__ == "__main__":
    app()
