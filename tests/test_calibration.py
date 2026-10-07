from agentsec.evaluators.calibration import CalibrationRow, compute_calibration


def test_calibration_computes_agreement_and_flags_small_sample() -> None:
    rows = [
        CalibrationRow(trace_id="trace-1", human_label="PASS", judge_label="PASS"),
        CalibrationRow(trace_id="trace-2", human_label="FAIL", judge_label="PASS"),
        CalibrationRow(trace_id="trace-3", human_label="FAIL", judge_label="FAIL"),
    ]

    report = compute_calibration(rows)

    assert report.sample_count == 3
    assert report.agreement_count == 2
    assert report.agreement_rate == 2 / 3
    assert report.cohen_kappa is not None
    assert report.disagreement_trace_ids == ["trace-2"]
    assert report.warning is not None
