"""Generate measurements and plots exclusively from saved SQLite trial rows."""

from __future__ import annotations

import json
import math
import sqlite3
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from agentsec.attacks.library import load_attack_library

_Z_95 = 1.959963984540054


def wilson_interval(successes: int, total: int, z: float = _Z_95) -> tuple[float, float] | None:
    """Return a two-sided Wilson score interval, or ``None`` for no observations."""

    if total <= 0:
        return None
    proportion = successes / total
    denominator = 1 + z * z / total
    center = (proportion + z * z / (2 * total)) / denominator
    margin = (
        z
        * math.sqrt(proportion * (1 - proportion) / total + z * z / (4 * total * total))
        / denominator
    )
    return max(0.0, center - margin), min(1.0, center + margin)


def _defense_label(raw: str) -> str:
    values = json.loads(raw)
    active = [value for value in values if value != "D0"]
    return "D0" if not active else "D0 + " + " + ".join(active)


def _load_rows(paths: list[Path]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    runs: list[dict[str, Any]] = []
    trials: list[dict[str, Any]] = []
    seen_trials: set[tuple[Any, ...]] = set()
    for path in paths:
        if not path.exists():
            continue
        with sqlite3.connect(path) as connection:
            connection.row_factory = sqlite3.Row
            try:
                records = connection.execute(
                    "SELECT r.id AS run_id,r.created_at,r.evaluation_type,r.backend,r.model,"
                    "r.temperature,r.seed,r.defenses_json,r.requested_trials,r.attack_count,"
                    "r.task_count,t.evaluation_type AS trial_type,t.task_id,t.attack_id,"
                    "t.category,t.mutation_type,t.trial_index,t.status,t.trace_json,t.elapsed_seconds,"
                    "t.prompt_tokens,t.completion_tokens "
                    "FROM runs r JOIN trial_results t ON r.id=t.run_id ORDER BY r.created_at"
                ).fetchall()
            except sqlite3.Error:
                continue
        seen_run_ids: set[str] = set()
        for row in records:
            record = dict(row)
            record["defense_label"] = _defense_label(record["defenses_json"])
            if record["run_id"] not in seen_run_ids:
                runs.append(record)
                seen_run_ids.add(record["run_id"])
            unique_key = (
                record["backend"],
                record["model"],
                record["temperature"],
                record["seed"],
                record["defenses_json"],
                record["trial_type"],
                record["task_id"],
                record["attack_id"],
                record["trial_index"],
            )
            if unique_key in seen_trials:
                continue
            seen_trials.add(unique_key)
            try:
                record["trace"] = json.loads(record["trace_json"])
            except (json.JSONDecodeError, TypeError):
                record["trace"] = {}
            trials.append(record)
    return runs, trials


def _rate_rows(
    trials: list[dict[str, Any]],
    *,
    field: str | None = None,
) -> list[tuple[str, int, int, float, float, float]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for trial in trials:
        if trial["trial_type"] != "attack":
            continue
        key = str(trial[field]) if field else trial["defense_label"]
        if field:
            key = f"{trial['defense_label']} / {key}"
        groups[key].append(trial)
    output = []
    for key, rows in sorted(groups.items()):
        observed = [row for row in rows if row["status"] in {"PASS", "FAIL"}]
        successes = sum(row["status"] == "FAIL" for row in observed)
        interval = wilson_interval(successes, len(observed))
        if interval is None:
            continue
        output.append(
            (
                key,
                len(observed),
                successes,
                successes / len(observed),
                interval[0],
                interval[1],
            )
        )
    return output


def _svg_plot(rows: list[tuple[str, int, int, float, float, float]], path: Path) -> None:
    width, height = 900, 470
    left, right, top, bottom = 70, 25, 30, 140
    chart_height = height - top - bottom
    chart_width = width - left - right
    count = max(1, len(rows))
    slot = chart_width / count
    bar_width = min(55.0, slot * 0.54)
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="450" y="22" text-anchor="middle" font-family="Arial" font-size="17">'
        "Attack success rate by defense (Wilson 95% CI)</text>",
    ]
    for tick in range(0, 101, 20):
        y = top + chart_height * (1 - tick / 100)
        svg.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{width - right}" y2="{y:.1f}" '
            'stroke="#dddddd" stroke-width="1"/>'
        )
        svg.append(
            f'<text x="{left - 10}" y="{y + 4:.1f}" text-anchor="end" '
            f'font-family="Arial" font-size="11">{tick}%</text>'
        )
    for index, (label, total, _success, rate, low, high) in enumerate(rows):
        center_x = left + slot * (index + 0.5)
        bar_x = center_x - bar_width / 2
        bar_y = top + chart_height * (1 - rate)
        bar_h = chart_height * rate
        svg.append(
            f'<rect x="{bar_x:.1f}" y="{bar_y:.1f}" width="{bar_width:.1f}" '
            f'height="{bar_h:.1f}" fill="#3366cc"/>'
        )
        low_y = top + chart_height * (1 - low)
        high_y = top + chart_height * (1 - high)
        svg.extend(
            [
                f'<line x1="{center_x:.1f}" y1="{high_y:.1f}" '
                f'x2="{center_x:.1f}" y2="{low_y:.1f}" stroke="#202020"/>',
                f'<line x1="{center_x - 6:.1f}" y1="{high_y:.1f}" '
                f'x2="{center_x + 6:.1f}" y2="{high_y:.1f}" stroke="#202020"/>',
                f'<line x1="{center_x - 6:.1f}" y1="{low_y:.1f}" '
                f'x2="{center_x + 6:.1f}" y2="{low_y:.1f}" stroke="#202020"/>',
                f'<text x="{center_x:.1f}" y="{height - bottom + 20}" text-anchor="middle" '
                f'font-family="Arial" font-size="10">{label}</text>',
                f'<text x="{center_x:.1f}" y="{height - bottom + 38}" text-anchor="middle" '
                f'font-family="Arial" font-size="10">n={total}</text>',
            ]
        )
    svg.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(svg), encoding="utf-8")


def generate_report(
    result_paths: list[Path],
    report_path: Path = Path("REPORT.md"),
    plot_path: Path | None = None,
) -> dict[str, int]:
    """Generate the Markdown report and a dependency-free SVG from saved runs."""

    runs, trials = _load_rows(result_paths)
    attacks = load_attack_library()
    attack_ids = {attack.id for attack in attacks}
    measured_attack_ids = {
        row["attack_id"] for row in trials if row["trial_type"] == "attack" and row["attack_id"]
    }
    defenses = sorted({row["defense_label"] for row in trials})
    overall = _rate_rows(trials)
    plot = plot_path or report_path.parent / "results" / "asr_by_defense.svg"
    if overall:
        _svg_plot(overall, plot)

    lines = [
        "# AgentSec Sandbox Experiment Report",
        "",
        "## Scope and method",
        "",
        "Results below are computed from trial rows stored in the listed SQLite databases. "
        "Attack success rate (ASR) is `FAIL / (PASS + FAIL)`; `ERROR` trials are excluded. "
        "Intervals are two-sided 95% Wilson score intervals. Benign success is `PASS / "
        "(PASS + FAIL)`. Latency and tokens are arithmetic means over observed trials.",
        "",
        f"Measured expanded attack IDs: **{len(measured_attack_ids)} / {len(attack_ids)}**; "
        f"defense configurations with saved trials: **{len(defenses)}**; "
        f"saved trial rows: **{len(trials)}**.",
        "",
    ]
    if overall:
        lines.extend(
            [
                "## Attack success",
                "",
                "| Defense stack | n | Attack successes | ASR | Wilson 95% CI | "
                "Mean seconds | Mean tokens |",
                "|---|---:|---:|---:|---:|---:|---:|",
            ]
        )
        by_defense = {label: [] for label in defenses}
        for row in trials:
            if row["trial_type"] == "attack":
                by_defense.setdefault(row["defense_label"], []).append(row)
        for label, count, successes, rate, low, high in overall:
            values = [row for row in by_defense[label] if row["status"] in {"PASS", "FAIL"}]
            seconds = mean(row["elapsed_seconds"] for row in values)
            tokens = mean(row["prompt_tokens"] + row["completion_tokens"] for row in values)
            lines.append(
                f"| {label} | {count} | {successes} | {rate:.1%} | "
                f"[{low:.1%}, {high:.1%}] | {seconds:.2f} | {tokens:.1f} |"
            )
        lines.extend(["", f"![ASR plot]({plot.relative_to(report_path.parent).as_posix()})", ""])
    else:
        lines.extend(["## Attack success", "", "No attack trial rows were found.", ""])

    category_rows = _rate_rows(
        [row for row in trials if row["trial_type"] == "attack"], field="category"
    )
    lines.extend(
        [
            "## Attack categories and mutations",
            "",
            "| Defense stack / category | n | Successes | ASR | Wilson 95% CI |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    if category_rows:
        for label, count, successes, rate, low, high in category_rows:
            lines.append(
                f"| {label} | {count} | {successes} | {rate:.1%} | [{low:.1%}, {high:.1%}] |"
            )
    else:
        lines.append("| No attack category results | 0 | 0 | N/A | N/A |")
    mutation_rows = _rate_rows(
        [row for row in trials if row["trial_type"] == "attack"], field="mutation_type"
    )
    if mutation_rows:
        lines.extend(
            [
                "",
                "### Mutation types",
                "",
                "| Defense stack / mutation | n | Successes | ASR | Wilson 95% CI |",
                "|---|---:|---:|---:|---:|",
            ]
        )
        for label, count, successes, rate, low, high in mutation_rows:
            lines.append(
                f"| {label} | {count} | {successes} | {rate:.1%} | [{low:.1%}, {high:.1%}] |"
            )

    benign_trials = [row for row in trials if row["trial_type"] == "benign"]
    benign_by_defense: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in benign_trials:
        benign_by_defense[row["defense_label"]].append(row)
    lines.extend(
        [
            "",
            "## Benign utility and blocking false positives",
            "",
            "| Defense stack | n | Successful tasks | Success rate | Wilson 95% CI | "
            "Blocked benign / FPR | Mean seconds | Mean tokens |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    if benign_by_defense:
        for label, records in sorted(benign_by_defense.items()):
            observed = [row for row in records if row["status"] in {"PASS", "FAIL"}]
            successes = sum(row["status"] == "PASS" for row in observed)
            interval = wilson_interval(successes, len(observed))
            blocked = sum(
                any(
                    event.get("event_type") == "defense_block"
                    for event in row["trace"].get("events", [])
                )
                for row in observed
            )
            if interval is None:
                lines.append(f"| {label} | 0 | 0 | N/A | N/A | N/A | N/A | N/A |")
            else:
                false_positive_rate = blocked / len(observed)
                seconds = mean(row["elapsed_seconds"] for row in observed)
                tokens = mean(row["prompt_tokens"] + row["completion_tokens"] for row in observed)
                lines.append(
                    f"| {label} | {len(observed)} | {successes} | "
                    f"{successes / len(observed):.1%} | "
                    f"[{interval[0]:.1%}, {interval[1]:.1%}] | "
                    f"{blocked}/{len(observed)} ({false_positive_rate:.1%}) | "
                    f"{seconds:.2f} | {tokens:.1f} |"
                )
    else:
        lines.append("| No benign runs recorded | 0 | 0 | N/A | N/A | N/A | N/A | N/A |")

    lines.extend(
        [
            "",
            "## OWASP and NIST crosswalk",
            "",
            "| Attack category | OWASP GenAI LLM Top 10 (2026) | NIST AI RMF GenAI Profile areas |",
            "|---|---|---|",
        ]
    )
    by_category: dict[str, dict[str, set[str]]] = {}
    for attack in attacks:
        entry = by_category.setdefault(attack.category.value, {"owasp": set(), "nist": set()})
        entry["owasp"].update(item.value for item in attack.mapped_owasp)
        entry["nist"].update(item.value for item in attack.mapped_nist)
    for category, mappings in sorted(by_category.items()):
        owasp = "; ".join(sorted(mappings["owasp"]))
        nist = "; ".join(sorted(mappings["nist"]))
        lines.append(f"| {category} | {owasp} | {nist} |")

    lines.extend(
        [
            "",
            "The crosswalk is an analyst-selected mapping from attack records, not an official "
            "one-to-one OWASP or NIST classification. OWASP numbering follows the 2026 edition. "
            "The NIST AI RMF Generative AI Profile organizes risks by profile risk areas; this "
            "mapping does not imply NIST certification.",
            "",
            "## Run inventory",
            "",
            "| Run ID | Type | Backend / model | Defense stack | Seed | Requested trials |",
            "|---|---|---|---|---:|---:|",
        ]
    )
    for run in runs:
        lines.append(
            f"| {run['run_id']} | {run['evaluation_type']} | {run['backend']} / {run['model']} | "
            f"{run['defense_label']} | {run['seed']} | {run['requested_trials']} |"
        )

    lines.extend(
        [
            "",
            "## Limitations and what did not work",
            "",
        ]
    )
    if len(measured_attack_ids) < len(attack_ids):
        lines.append(
            f"- Coverage is incomplete: only {len(measured_attack_ids)} of {len(attack_ids)} "
            "expanded attack IDs have saved trial results. Do not interpret these samples as "
            "full-corpus performance."
        )
    if not benign_trials:
        lines.append("- No benign utility or blocking false-positive run has been recorded.")
    if "D5" not in defenses:
        lines.append("- D5 context-isolation model overhead has not been measured in saved runs.")
    else:
        lines.append(
            "- D5 timing and token use are measured only on one attack sample; its overhead "
            "estimate is preliminary."
        )
    if len(defenses) < 12 or len(measured_attack_ids) < len(attack_ids):
        lines.append(
            "- The full ablation is incomplete: it requires the entire expanded attack corpus "
            "under all 12 configurations; unmeasured cases are omitted."
        )
    if not lines[-1].startswith("-"):
        lines.append("- No additional limitations were inferred from the stored run inventory.")
    lines.extend(
        [
            "- The current evaluator is deterministic and uses declared trace criteria; no LLM "
            "judge labels are included. Human calibration remains pending paired annotations.",
            "- Local Ollama timings and behavior are specific to the recorded model, machine, "
            "temperature, and seeds. The mock email tool writes only to its local in-memory "
            "outbox.",
            "",
            "## Reproduction",
            "",
            "Use `agentsec reproduce` with the same backend and model configuration to run the "
            "default full ablation. Each trial is committed to SQLite as it completes; rerunning "
            "with the same database resumes missing or errored cases. `agentsec report` rebuilds "
            "this document and the SVG using saved data only.",
            "",
            "Sources: [OWASP GenAI LLM Top 10 (2026)]"
            "(https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/); "
            "[NIST AI RMF Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf).",
            "",
        ]
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return {"runs": len(runs), "trials": len(trials), "attack_ids": len(measured_attack_ids)}
