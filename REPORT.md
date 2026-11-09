# AgentSec Sandbox Experiment Report

## Scope and method

Results below are computed from trial rows stored in the listed SQLite databases. Attack success rate (ASR) is `FAIL / (PASS + FAIL)`; `ERROR` trials are excluded. Intervals are two-sided 95% Wilson score intervals. Benign success is `PASS / (PASS + FAIL)`. Latency and tokens are arithmetic means over observed trials.

Measured expanded attack IDs: **640 / 640**; defense configurations with saved trials: **12**; saved trial rows: **4593**.

## Attack success

| Defense stack | n | Attack successes | ASR | Wilson 95% CI | Mean seconds | Mean tokens |
|---|---:|---:|---:|---:|---:|---:|
| D0 | 533 | 44 | 8.3% | [6.2%, 10.9%] | 2.90 | 713.8 |
| D0 + D1 | 533 | 36 | 6.8% | [4.9%, 9.2%] | 2.08 | 770.4 |
| D0 + D1 + D2 | 456 | 0 | 0.0% | [0.0%, 0.8%] | 2.40 | 578.2 |
| D0 + D1 + D2 + D3 | 640 | 1 | 0.2% | [0.0%, 0.9%] | 1.78 | 558.2 |
| D0 + D1 + D2 + D3 + D4 | 98 | 0 | 0.0% | [0.0%, 3.8%] | 1.66 | 573.8 |
| D0 + D1 + D2 + D3 + D4 + D5 | 640 | 1 | 0.2% | [0.0%, 0.9%] | 2.55 | 723.1 |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 | 640 | 1 | 0.2% | [0.0%, 0.9%] | 2.57 | 723.1 |
| D0 + D2 | 82 | 0 | 0.0% | [0.0%, 4.5%] | 2.21 | 452.8 |
| D0 + D3 | 65 | 0 | 0.0% | [0.0%, 5.6%] | 2.94 | 615.0 |
| D0 + D4 | 106 | 0 | 0.0% | [0.0%, 3.5%] | 2.74 | 725.0 |
| D0 + D5 | 568 | 0 | 0.0% | [0.0%, 0.7%] | 2.86 | 783.0 |
| D0 + D6 | 82 | 0 | 0.0% | [0.0%, 4.5%] | 2.38 | 697.8 |

![ASR plot](results/asr_by_defense.svg)

## Attack categories and mutations

| Defense stack / category | n | Successes | ASR | Wilson 95% CI |
|---|---:|---:|---:|---:|
| D0 + D1 + D2 + D3 + D4 + D5 + D6 / data_exfiltration | 80 | 1 | 1.2% | [0.2%, 6.7%] |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 / direct_prompt_injection | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 / indirect_document | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 / indirect_webpage | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 / malicious_tool_output | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 / memory_poisoning | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 / privilege_escalation | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 / tool_poisoning | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 / data_exfiltration | 80 | 1 | 1.2% | [0.2%, 6.7%] |
| D0 + D1 + D2 + D3 + D4 + D5 / direct_prompt_injection | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 / indirect_document | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 / indirect_webpage | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 / malicious_tool_output | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 / memory_poisoning | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 / privilege_escalation | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 / tool_poisoning | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 / direct_prompt_injection | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 / indirect_webpage | 18 | 0 | 0.0% | [0.0%, 17.6%] |
| D0 + D1 + D2 + D3 / data_exfiltration | 80 | 1 | 1.2% | [0.2%, 6.7%] |
| D0 + D1 + D2 + D3 / direct_prompt_injection | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 / indirect_document | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 / indirect_webpage | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 / malicious_tool_output | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 / memory_poisoning | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 / privilege_escalation | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 / tool_poisoning | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 / direct_prompt_injection | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 / indirect_document | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 / indirect_webpage | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 / malicious_tool_output | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 / privilege_escalation | 56 | 0 | 0.0% | [0.0%, 6.4%] |
| D0 + D1 + D2 / tool_poisoning | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 / data_exfiltration | 53 | 5 | 9.4% | [4.1%, 20.3%] |
| D0 + D1 / direct_prompt_injection | 80 | 10 | 12.5% | [6.9%, 21.5%] |
| D0 + D1 / indirect_document | 80 | 2 | 2.5% | [0.7%, 8.7%] |
| D0 + D1 / indirect_webpage | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 / malicious_tool_output | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 / privilege_escalation | 80 | 19 | 23.8% | [15.8%, 34.1%] |
| D0 + D1 / tool_poisoning | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D2 / direct_prompt_injection | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D2 / indirect_webpage | 2 | 0 | 0.0% | [0.0%, 65.8%] |
| D0 + D3 / direct_prompt_injection | 65 | 0 | 0.0% | [0.0%, 5.6%] |
| D0 + D4 / direct_prompt_injection | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D4 / indirect_webpage | 26 | 0 | 0.0% | [0.0%, 12.9%] |
| D0 + D5 / data_exfiltration | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D5 / direct_prompt_injection | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D5 / indirect_document | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D5 / indirect_webpage | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D5 / malicious_tool_output | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D5 / memory_poisoning | 8 | 0 | 0.0% | [0.0%, 32.4%] |
| D0 + D5 / privilege_escalation | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D5 / tool_poisoning | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D6 / direct_prompt_injection | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D6 / indirect_webpage | 2 | 0 | 0.0% | [0.0%, 65.8%] |
| D0 / data_exfiltration | 53 | 4 | 7.5% | [3.0%, 17.9%] |
| D0 / direct_prompt_injection | 80 | 12 | 15.0% | [8.8%, 24.4%] |
| D0 / indirect_document | 80 | 3 | 3.8% | [1.3%, 10.5%] |
| D0 / indirect_webpage | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 / malicious_tool_output | 80 | 1 | 1.2% | [0.2%, 6.7%] |
| D0 / privilege_escalation | 80 | 24 | 30.0% | [21.1%, 40.8%] |
| D0 / tool_poisoning | 80 | 0 | 0.0% | [0.0%, 4.6%] |

### Mutation types

| Defense stack / mutation | n | Successes | ASR | Wilson 95% CI |
|---|---:|---:|---:|---:|
| D0 + D1 + D2 + D3 + D4 + D5 + D6 / base | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 / delimiter_confusion | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 / encoding_base64 | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 / encoding_rot13 | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 / instruction_hiding | 80 | 1 | 1.2% | [0.2%, 6.7%] |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 / language_switch | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 / payload_splitting | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 / role_play | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 / base | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 / delimiter_confusion | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 / encoding_base64 | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 / encoding_rot13 | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 / instruction_hiding | 80 | 1 | 1.2% | [0.2%, 6.7%] |
| D0 + D1 + D2 + D3 + D4 + D5 / language_switch | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 / payload_splitting | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 + D5 / role_play | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 + D4 / base | 13 | 0 | 0.0% | [0.0%, 22.8%] |
| D0 + D1 + D2 + D3 + D4 / delimiter_confusion | 12 | 0 | 0.0% | [0.0%, 24.2%] |
| D0 + D1 + D2 + D3 + D4 / encoding_base64 | 12 | 0 | 0.0% | [0.0%, 24.2%] |
| D0 + D1 + D2 + D3 + D4 / encoding_rot13 | 12 | 0 | 0.0% | [0.0%, 24.2%] |
| D0 + D1 + D2 + D3 + D4 / instruction_hiding | 13 | 0 | 0.0% | [0.0%, 22.8%] |
| D0 + D1 + D2 + D3 + D4 / language_switch | 12 | 0 | 0.0% | [0.0%, 24.2%] |
| D0 + D1 + D2 + D3 + D4 / payload_splitting | 12 | 0 | 0.0% | [0.0%, 24.2%] |
| D0 + D1 + D2 + D3 + D4 / role_play | 12 | 0 | 0.0% | [0.0%, 24.2%] |
| D0 + D1 + D2 + D3 / base | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 / delimiter_confusion | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 / encoding_base64 | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 / encoding_rot13 | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 / instruction_hiding | 80 | 1 | 1.2% | [0.2%, 6.7%] |
| D0 + D1 + D2 + D3 / language_switch | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 / payload_splitting | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 + D3 / role_play | 80 | 0 | 0.0% | [0.0%, 4.6%] |
| D0 + D1 + D2 / base | 57 | 0 | 0.0% | [0.0%, 6.3%] |
| D0 + D1 + D2 / delimiter_confusion | 57 | 0 | 0.0% | [0.0%, 6.3%] |
| D0 + D1 + D2 / encoding_base64 | 57 | 0 | 0.0% | [0.0%, 6.3%] |
| D0 + D1 + D2 / encoding_rot13 | 57 | 0 | 0.0% | [0.0%, 6.3%] |
| D0 + D1 + D2 / instruction_hiding | 57 | 0 | 0.0% | [0.0%, 6.3%] |
| D0 + D1 + D2 / language_switch | 57 | 0 | 0.0% | [0.0%, 6.3%] |
| D0 + D1 + D2 / payload_splitting | 57 | 0 | 0.0% | [0.0%, 6.3%] |
| D0 + D1 + D2 / role_play | 57 | 0 | 0.0% | [0.0%, 6.3%] |
| D0 + D1 / base | 67 | 7 | 10.4% | [5.2%, 20.0%] |
| D0 + D1 / delimiter_confusion | 66 | 4 | 6.1% | [2.4%, 14.6%] |
| D0 + D1 / encoding_base64 | 67 | 0 | 0.0% | [0.0%, 5.4%] |
| D0 + D1 / encoding_rot13 | 67 | 0 | 0.0% | [0.0%, 5.4%] |
| D0 + D1 / instruction_hiding | 67 | 3 | 4.5% | [1.5%, 12.4%] |
| D0 + D1 / language_switch | 67 | 10 | 14.9% | [8.3%, 25.3%] |
| D0 + D1 / payload_splitting | 66 | 7 | 10.6% | [5.2%, 20.3%] |
| D0 + D1 / role_play | 66 | 5 | 7.6% | [3.3%, 16.5%] |
| D0 + D2 / base | 11 | 0 | 0.0% | [0.0%, 25.9%] |
| D0 + D2 / delimiter_confusion | 10 | 0 | 0.0% | [0.0%, 27.8%] |
| D0 + D2 / encoding_base64 | 10 | 0 | 0.0% | [0.0%, 27.8%] |
| D0 + D2 / encoding_rot13 | 10 | 0 | 0.0% | [0.0%, 27.8%] |
| D0 + D2 / instruction_hiding | 11 | 0 | 0.0% | [0.0%, 25.9%] |
| D0 + D2 / language_switch | 10 | 0 | 0.0% | [0.0%, 27.8%] |
| D0 + D2 / payload_splitting | 10 | 0 | 0.0% | [0.0%, 27.8%] |
| D0 + D2 / role_play | 10 | 0 | 0.0% | [0.0%, 27.8%] |
| D0 + D3 / base | 9 | 0 | 0.0% | [0.0%, 29.9%] |
| D0 + D3 / delimiter_confusion | 8 | 0 | 0.0% | [0.0%, 32.4%] |
| D0 + D3 / encoding_base64 | 7 | 0 | 0.0% | [0.0%, 35.4%] |
| D0 + D3 / encoding_rot13 | 8 | 0 | 0.0% | [0.0%, 32.4%] |
| D0 + D3 / instruction_hiding | 9 | 0 | 0.0% | [0.0%, 29.9%] |
| D0 + D3 / language_switch | 8 | 0 | 0.0% | [0.0%, 32.4%] |
| D0 + D3 / payload_splitting | 8 | 0 | 0.0% | [0.0%, 32.4%] |
| D0 + D3 / role_play | 8 | 0 | 0.0% | [0.0%, 32.4%] |
| D0 + D4 / base | 14 | 0 | 0.0% | [0.0%, 21.5%] |
| D0 + D4 / delimiter_confusion | 13 | 0 | 0.0% | [0.0%, 22.8%] |
| D0 + D4 / encoding_base64 | 13 | 0 | 0.0% | [0.0%, 22.8%] |
| D0 + D4 / encoding_rot13 | 13 | 0 | 0.0% | [0.0%, 22.8%] |
| D0 + D4 / instruction_hiding | 14 | 0 | 0.0% | [0.0%, 21.5%] |
| D0 + D4 / language_switch | 13 | 0 | 0.0% | [0.0%, 22.8%] |
| D0 + D4 / payload_splitting | 13 | 0 | 0.0% | [0.0%, 22.8%] |
| D0 + D4 / role_play | 13 | 0 | 0.0% | [0.0%, 22.8%] |
| D0 + D5 / base | 71 | 0 | 0.0% | [0.0%, 5.1%] |
| D0 + D5 / delimiter_confusion | 71 | 0 | 0.0% | [0.0%, 5.1%] |
| D0 + D5 / encoding_base64 | 71 | 0 | 0.0% | [0.0%, 5.1%] |
| D0 + D5 / encoding_rot13 | 71 | 0 | 0.0% | [0.0%, 5.1%] |
| D0 + D5 / instruction_hiding | 71 | 0 | 0.0% | [0.0%, 5.1%] |
| D0 + D5 / language_switch | 71 | 0 | 0.0% | [0.0%, 5.1%] |
| D0 + D5 / payload_splitting | 71 | 0 | 0.0% | [0.0%, 5.1%] |
| D0 + D5 / role_play | 71 | 0 | 0.0% | [0.0%, 5.1%] |
| D0 + D6 / base | 11 | 0 | 0.0% | [0.0%, 25.9%] |
| D0 + D6 / delimiter_confusion | 10 | 0 | 0.0% | [0.0%, 27.8%] |
| D0 + D6 / encoding_base64 | 10 | 0 | 0.0% | [0.0%, 27.8%] |
| D0 + D6 / encoding_rot13 | 10 | 0 | 0.0% | [0.0%, 27.8%] |
| D0 + D6 / instruction_hiding | 11 | 0 | 0.0% | [0.0%, 25.9%] |
| D0 + D6 / language_switch | 10 | 0 | 0.0% | [0.0%, 27.8%] |
| D0 + D6 / payload_splitting | 10 | 0 | 0.0% | [0.0%, 27.8%] |
| D0 + D6 / role_play | 10 | 0 | 0.0% | [0.0%, 27.8%] |
| D0 / base | 67 | 9 | 13.4% | [7.2%, 23.6%] |
| D0 / delimiter_confusion | 66 | 5 | 7.6% | [3.3%, 16.5%] |
| D0 / encoding_base64 | 67 | 0 | 0.0% | [0.0%, 5.4%] |
| D0 / encoding_rot13 | 67 | 0 | 0.0% | [0.0%, 5.4%] |
| D0 / instruction_hiding | 67 | 5 | 7.5% | [3.2%, 16.3%] |
| D0 / language_switch | 67 | 10 | 14.9% | [8.3%, 25.3%] |
| D0 / payload_splitting | 66 | 10 | 15.2% | [8.4%, 25.7%] |
| D0 / role_play | 66 | 5 | 7.6% | [3.3%, 16.5%] |

## Benign utility and blocking false positives

| Defense stack | n | Successful tasks | Success rate | Wilson 95% CI | Blocked benign / FPR | Mean seconds | Mean tokens |
|---|---:|---:|---:|---:|---:|
| D0 | 20 | 5 | 25.0% | [11.2%, 46.9%] | 0/20 (0.0%) | 2.51 | 615.8 |
| D0 + D1 | 20 | 7 | 35.0% | [18.1%, 56.7%] | 0/20 (0.0%) | 2.03 | 724.5 |
| D0 + D2 | 20 | 10 | 50.0% | [29.9%, 70.1%] | 0/20 (0.0%) | 2.10 | 375.6 |
| D0 + D3 | 20 | 6 | 30.0% | [14.5%, 51.9%] | 0/20 (0.0%) | 2.21 | 647.1 |
| D0 + D4 | 20 | 5 | 25.0% | [11.2%, 46.9%] | 0/20 (0.0%) | 2.34 | 617.8 |
| D0 + D5 | 20 | 7 | 35.0% | [18.1%, 56.7%] | 0/20 (0.0%) | 2.26 | 669.9 |
| D0 + D6 | 20 | 5 | 25.0% | [11.2%, 46.9%] | 0/20 (0.0%) | 2.31 | 615.9 |

## OWASP and NIST crosswalk

| Attack category | OWASP GenAI LLM Top 10 (2026) | NIST AI RMF GenAI Profile areas |
|---|---|---|
| data_exfiltration | LLM02:2026 Sensitive Information Disclosure; LLM03:2026 Excessive Agency | NIST AI RMF GenAI Profile: Data Privacy; NIST AI RMF GenAI Profile: Information Security |
| direct_prompt_injection | LLM01:2026 Prompt Injection; LLM03:2026 Excessive Agency | NIST AI RMF GenAI Profile: Human-AI Configuration; NIST AI RMF GenAI Profile: Information Security |
| indirect_document | LLM01:2026 Prompt Injection; LLM02:2026 Sensitive Information Disclosure | NIST AI RMF GenAI Profile: Information Integrity; NIST AI RMF GenAI Profile: Information Security |
| indirect_webpage | LLM01:2026 Prompt Injection; LLM02:2026 Sensitive Information Disclosure | NIST AI RMF GenAI Profile: Information Integrity; NIST AI RMF GenAI Profile: Information Security |
| malicious_tool_output | LLM01:2026 Prompt Injection; LLM03:2026 Excessive Agency | NIST AI RMF GenAI Profile: Information Integrity; NIST AI RMF GenAI Profile: Information Security |
| memory_poisoning | LLM01:2026 Prompt Injection; LLM05:2026 Data and Model Poisoning; LLM08:2026 Hidden Context Exposure | NIST AI RMF GenAI Profile: Human-AI Configuration; NIST AI RMF GenAI Profile: Information Integrity |
| privilege_escalation | LLM01:2026 Prompt Injection; LLM03:2026 Excessive Agency | NIST AI RMF GenAI Profile: Human-AI Configuration; NIST AI RMF GenAI Profile: Information Security |
| tool_poisoning | LLM01:2026 Prompt Injection; LLM03:2026 Excessive Agency; LLM04:2026 Supply Chain | NIST AI RMF GenAI Profile: Information Security; NIST AI RMF GenAI Profile: Value Chain and Component Integration |

The crosswalk is an analyst-selected mapping from attack records, not an official one-to-one OWASP or NIST classification. OWASP numbering follows the 2026 edition. The NIST AI RMF Generative AI Profile organizes risks by profile risk areas; this mapping does not imply NIST certification.

## Run inventory

| Run ID | Type | Backend / model | Defense stack | Seed | Requested trials |
|---|---|---|---|---:|---:|
| c7632b9df0b841618d6f9b79b8df6d7d | attack | ollama / llama3.1:8b | D0 | 42 | 1 |
| beb55eec3bb64f188bd58320d346b8a7 | attack | ollama / llama3.1:8b | D0 + D1 | 42 | 1 |
| 14b08c8df21c43a9860d45c76e7abc90 | attack | ollama / llama3.1:8b | D0 + D2 | 42 | 1 |
| 23f252f2c9644105b94cc49ab9311224 | attack | ollama / llama3.1:8b | D0 + D3 | 42 | 1 |
| 4cc1667ca57a4255b61c15c41808016d | attack | ollama / llama3.1:8b | D0 + D4 | 42 | 1 |
| 3fdbafd6446f459d819e176d7f98a7c1 | attack | ollama / llama3.1:8b | D0 + D5 | 42 | 1 |
| 5e5e033de95f4dd2a2e1ae0e5d9d74fa | attack | ollama / llama3.1:8b | D0 + D6 | 42 | 1 |
| ff23feff32524211b3ede47e3627d751 | attack | ollama / llama3.1:8b | D0 + D1 + D2 | 42 | 1 |
| adf9098f83264c96bb72e75147834fc8 | attack | ollama / llama3.1:8b | D0 + D1 + D2 + D3 | 42 | 1 |
| 4d4f9ba636014432951c579e90ebc63f | attack | ollama / llama3.1:8b | D0 + D1 + D2 + D3 + D4 | 42 | 1 |
| 6ca6b9d9e10d4dd28f3e6caded568d9e | attack | ollama / llama3.1:8b | D0 + D1 + D2 + D3 + D4 + D5 | 42 | 1 |
| a0bd3750c2bc4de4baf4bc956e3d572a | attack | ollama / llama3.1:8b | D0 + D1 + D2 + D3 + D4 + D5 + D6 | 42 | 1 |
| 60a0ee8075064845bfc79c84bdb328af | attack | ollama / llama3.1:8b | D0 | 42 | 1 |
| d04c2eab850848b890bb1769f7b265dd | attack | ollama / llama3.1:8b | D0 + D1 | 42 | 1 |
| 7d390d9403ff4fc6b1779ee8b83e2a15 | attack | ollama / llama3.1:8b | D0 + D2 | 42 | 1 |
| f0556fc329be427c8af0d5f7d92e444e | attack | ollama / llama3.1:8b | D0 + D3 | 42 | 1 |
| b4db2295aec34310b02445cf8ca08ac6 | attack | ollama / llama3.1:8b | D0 + D4 | 42 | 1 |
| c540c1169f8a4ea59a5292b2e664265f | attack | ollama / llama3.1:8b | D0 + D5 | 42 | 1 |
| 0f90e56845644ee1a58f5a4e84df799b | attack | ollama / llama3.1:8b | D0 + D6 | 42 | 1 |
| 5a0bff3383b947d198e7feb1b2f20c2e | attack | ollama / llama3.1:8b | D0 + D1 + D2 | 42 | 1 |
| 24e5f71c57ba49928773a61715a1b066 | attack | ollama / llama3.1:8b | D0 + D1 + D2 + D3 | 42 | 1 |
| bf9439bb412849b0b3496fb64a0755f7 | attack | ollama / llama3.1:8b | D0 + D1 + D2 + D3 + D4 | 42 | 1 |
| 10bd4e31bc2d4d15accfff043ccbbfba | attack | ollama / llama3.1:8b | D0 + D1 + D2 + D3 + D4 + D5 | 42 | 1 |
| a75aed203ce744da9a392b4cc03d4dda | attack | ollama / llama3.1:8b | D0 + D1 + D2 + D3 + D4 + D5 + D6 | 42 | 1 |
| c097fbddd17744cc82ed45237c559bd8 | benign | ollama / llama3.1:8b | D0 | 42 | 1 |
| 878fbe8466cc4dce880340e6bf12472c | benign | ollama / llama3.1:8b | D0 + D1 | 42 | 1 |
| 579d635229a5495cbe55ea48a4c4eeac | benign | ollama / llama3.1:8b | D0 + D2 | 42 | 1 |
| 99b873b5e20c467d89aaf089269ef268 | benign | ollama / llama3.1:8b | D0 + D3 | 42 | 1 |
| 9b2f95bcd70849b99382ce1e1a7647ff | benign | ollama / llama3.1:8b | D0 + D4 | 42 | 1 |
| f6e97d2a87df4b9d8268e48a1b79611d | benign | ollama / llama3.1:8b | D0 + D5 | 42 | 1 |
| 53c967db5241480c8b4948aa6497b43c | benign | ollama / llama3.1:8b | D0 + D6 | 42 | 1 |
| de199067d32340558ca6b2180893bfcc | attack | ollama / llama3.1:8b | D0 | 42 | 1 |
| 40a7b1b821b64e55b16528cd85341888 | attack | ollama / llama3.1:8b | D0 | 42 | 1 |
| 7fc9aed888064587889f5c377b659e1b | attack | ollama / llama3.1:8b | D0 | 42 | 1 |
| 1391f3300aed423d9b61a0e96483c8af | attack | ollama / llama3.1:8b | D0 + D1 | 42 | 1 |
| 9656e53de59545fdbd2be99fdba268b9 | attack | ollama / llama3.1:8b | D0 + D2 | 42 | 1 |
| 4cfa051919d34228bdb550fcd450dbbb | attack | ollama / llama3.1:8b | D0 + D3 | 42 | 1 |
| 9c3a4bcbe4f0444d891fc5b6486fac7d | attack | ollama / llama3.1:8b | D0 + D4 | 42 | 1 |
| 94011c9c771241ecaea3d81ed0e21eed | attack | ollama / llama3.1:8b | D0 + D5 | 42 | 1 |
| c5ff826e452c46c0b35b31429338de2c | attack | ollama / llama3.1:8b | D0 + D6 | 42 | 1 |
| a7bd13e32d1146f690afc2093711c989 | attack | ollama / llama3.1:8b | D0 + D1 + D2 | 42 | 1 |
| 0e3e7d6ebf714e48b32387decc528015 | attack | ollama / llama3.1:8b | D0 + D1 + D2 + D3 | 42 | 1 |
| edfb76f50f5643ea9e7a76e83e81aff6 | attack | ollama / llama3.1:8b | D0 + D1 + D2 + D3 + D4 | 42 | 1 |
| 4342b17204d644569e9a9c0438b014f4 | attack | ollama / llama3.1:8b | D0 + D1 + D2 + D3 + D4 + D5 | 42 | 1 |
| 48733a168f7844db9ed71dbdf3b7f7be | attack | ollama / llama3.1:8b | D0 + D1 + D2 + D3 + D4 + D5 + D6 | 42 | 1 |
| 5117febdd35d4f63b6abae717473b5d9 | benign | ollama / llama3.1:8b | D0 | 42 | 1 |
| 9a1216c8a2c6474193e4863ca3145dfc | benign | ollama / llama3.1:8b | D0 + D1 | 42 | 1 |
| a63bfaff0b094668bbbc7097295869ff | benign | ollama / llama3.1:8b | D0 + D2 | 42 | 1 |
| 4295d77d915e4947b658ff1c5fd7d466 | benign | ollama / llama3.1:8b | D0 + D3 | 42 | 1 |
| a08de55248f34ed79b51d0018dcb1991 | benign | ollama / llama3.1:8b | D0 + D4 | 42 | 1 |
| 4bf02ced257a4137aea757fa5288cae8 | benign | ollama / llama3.1:8b | D0 + D5 | 42 | 1 |
| 98e4a28760244b07bf636bdddfadba97 | benign | ollama / llama3.1:8b | D0 + D6 | 42 | 1 |

## Limitations and what did not work

- D5 context-isolation model overhead has not been measured in saved runs.
- The current evaluator is deterministic and uses declared trace criteria; no LLM judge labels are included. Human calibration remains pending paired annotations.
- Local Ollama timings and behavior are specific to the recorded model, machine, temperature, and seeds. The mock email tool writes only to its local in-memory outbox.

## Reproduction

Use `agentsec reproduce` with the same backend and model configuration to run the default full ablation. Each trial is committed to SQLite as it completes; rerunning with the same database resumes missing or errored cases. `agentsec report` rebuilds this document and the SVG using saved data only.

Sources: [OWASP GenAI LLM Top 10 (2026)](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/); [NIST AI RMF Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf).
