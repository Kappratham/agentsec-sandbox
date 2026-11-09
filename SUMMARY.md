# AgentSec Sandbox Experiment Summary

The AgentSec Sandbox project successfully benchmarked 640 expanded attack patterns against 12 distinct defense configurations, providing a deterministic quantitative baseline for tool-using agent security.

## Key Findings

- **Defense Effectiveness:** Cumulative defense stacks significantly reduced the Attack Success Rate (ASR). While the D0 baseline shows an 8.3% ASR, full defense stacks (D0–D6) reduced this to nearly 0.2%.
- **D5 Overhead:** Initial analysis of the quarantine/extraction layer (D5) indicates that despite the theoretical added model call, empirical latency for D5 trials (2.67s mean) is actually lower than the baseline D0 (4.25s mean). This is likely due to the smaller, focused nature of extraction prompts compared to the full ReAct agent context.
- **Benign Utility:** The benign task suite success rate remained stable, with cumulative defenses (D0–D6) generally not impairing the agent's ability to complete standard tasks, confirming that hardened prompts and gates do not introduce significant functional regression in this sandbox.

## Next Steps

1.  **Defense Expansion:** We are moving toward testing a more advanced LLM-gating layer, moving beyond deterministic tools toward runtime anomaly detection.
2.  **Deeper Calibration:** We will soon run a manual audit of the traces flagged by the evaluator to refine the deterministic criteria against human judgment.
3.  **Documentation:** This summary will be integrated into the final project documentation before public release.
