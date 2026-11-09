# AgentSec Sandbox Experiment Report

## Scope and method

Results below are computed from trial rows stored in the listed SQLite databases. Attack success rate (ASR) is `FAIL / (PASS + FAIL)`; `ERROR` trials are excluded. Intervals are two-sided 95% Wilson score intervals. Benign success is `PASS / (PASS + FAIL)`. Latency and tokens are arithmetic means over observed trials.

Measured expanded attack IDs: **640 / 640**; defense configurations with saved trials: **15**; saved trial rows: **10294**.

## Attack success

| Defense stack | n | Attack successes | ASR | Wilson 95% CI | Mean seconds | Mean tokens |
|---|---:|---:|---:|---:|---:|---:|
| D0 | 2837 | 224 | 7.9% | [7.0%, 8.9%] | 2.84 | 709.6 |
| D0 + D1 | 2665 | 176 | 6.6% | [5.7%, 7.6%] | 2.03 | 771.7 |
| D0 + D1 + D2 | 456 | 0 | 0.0% | [0.0%, 0.8%] | 2.40 | 578.2 |
| D0 + D1 + D2 + D3 | 640 | 1 | 0.2% | [0.0%, 0.9%] | 1.78 | 558.2 |
| D0 + D1 + D2 + D3 + D4 | 98 | 0 | 0.0% | [0.0%, 3.8%] | 1.66 | 573.8 |
| D0 + D1 + D2 + D3 + D4 + D5 | 640 | 1 | 0.2% | [0.0%, 0.9%] | 2.55 | 723.1 |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 | 640 | 1 | 0.2% | [0.0%, 0.9%] | 2.57 | 723.1 |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 + D7 | 64 | 0 | 0.0% | [0.0%, 5.7%] | 3.51 | 750.3 |
| D0 + D2 | 692 | 0 | 0.0% | [0.0%, 0.6%] | 4.84 | 499.1 |
| D0 + D3 | 176 | 0 | 0.0% | [0.0%, 2.1%] | 2.87 | 618.1 |
| D0 + D4 | 254 | 0 | 0.0% | [0.0%, 1.5%] | 2.47 | 705.0 |
| D0 + D5 | 568 | 0 | 0.0% | [0.0%, 0.7%] | 2.86 | 783.0 |
| D0 + D6 | 82 | 0 | 0.0% | [0.0%, 4.5%] | 2.38 | 697.8 |
| D0 + D7 | 64 | 6 | 9.4% | [4.4%, 19.0%] | 3.54 | 697.3 |

![ASR plot](results/asr_by_defense.svg)

## Attack categories and mutations

| Defense stack / category | n | Successes | ASR | Wilson 95% CI |
|---|---:|---:|---:|---:|
| D0 + D1 + D2 + D3 + D4 + D5 + D6 + D7 / direct_prompt_injection | 64 | 0 | 0.0% | [0.0%, 5.7%] |
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
| D0 + D1 / data_exfiltration | 265 | 25 | 9.4% | [6.5%, 13.6%] |
| D0 + D1 / direct_prompt_injection | 400 | 50 | 12.5% | [9.6%, 16.1%] |
| D0 + D1 / indirect_document | 400 | 8 | 2.0% | [1.0%, 3.9%] |
| D0 + D1 / indirect_webpage | 400 | 0 | 0.0% | [0.0%, 1.0%] |
| D0 + D1 / malicious_tool_output | 400 | 0 | 0.0% | [0.0%, 1.0%] |
| D0 + D1 / privilege_escalation | 400 | 93 | 23.2% | [19.4%, 27.6%] |
| D0 + D1 / tool_poisoning | 400 | 0 | 0.0% | [0.0%, 1.0%] |
| D0 + D2 / direct_prompt_injection | 400 | 0 | 0.0% | [0.0%, 1.0%] |
| D0 + D2 / indirect_webpage | 292 | 0 | 0.0% | [0.0%, 1.3%] |
| D0 + D3 / direct_prompt_injection | 176 | 0 | 0.0% | [0.0%, 2.1%] |
| D0 + D4 / direct_prompt_injection | 228 | 0 | 0.0% | [0.0%, 1.7%] |
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
| D0 + D7 / direct_prompt_injection | 64 | 6 | 9.4% | [4.4%, 19.0%] |
| D0 / data_exfiltration | 395 | 28 | 7.1% | [4.9%, 10.1%] |
| D0 / direct_prompt_injection | 400 | 61 | 15.2% | [12.1%, 19.1%] |
| D0 / indirect_document | 400 | 11 | 2.8% | [1.5%, 4.9%] |
| D0 / indirect_webpage | 398 | 0 | 0.0% | [0.0%, 1.0%] |
| D0 / malicious_tool_output | 400 | 5 | 1.2% | [0.5%, 2.9%] |
| D0 / memory_poisoning | 44 | 0 | 0.0% | [0.0%, 8.0%] |
| D0 / privilege_escalation | 400 | 119 | 29.8% | [25.5%, 34.4%] |
| D0 / tool_poisoning | 400 | 0 | 0.0% | [0.0%, 1.0%] |

### Mutation types

| Defense stack / mutation | n | Successes | ASR | Wilson 95% CI |
|---|---:|---:|---:|---:|
| D0 + D1 + D2 + D3 + D4 + D5 + D6 + D7 / base | 8 | 0 | 0.0% | [0.0%, 32.4%] |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 + D7 / delimiter_confusion | 8 | 0 | 0.0% | [0.0%, 32.4%] |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 + D7 / encoding_base64 | 8 | 0 | 0.0% | [0.0%, 32.4%] |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 + D7 / encoding_rot13 | 8 | 0 | 0.0% | [0.0%, 32.4%] |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 + D7 / instruction_hiding | 8 | 0 | 0.0% | [0.0%, 32.4%] |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 + D7 / language_switch | 8 | 0 | 0.0% | [0.0%, 32.4%] |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 + D7 / payload_splitting | 8 | 0 | 0.0% | [0.0%, 32.4%] |
| D0 + D1 + D2 + D3 + D4 + D5 + D6 + D7 / role_play | 8 | 0 | 0.0% | [0.0%, 32.4%] |
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
| D0 + D1 / base | 335 | 35 | 10.4% | [7.6%, 14.2%] |
| D0 + D1 / delimiter_confusion | 330 | 20 | 6.1% | [4.0%, 9.2%] |
| D0 + D1 / encoding_base64 | 335 | 0 | 0.0% | [0.0%, 1.1%] |
| D0 + D1 / encoding_rot13 | 335 | 0 | 0.0% | [0.0%, 1.1%] |
| D0 + D1 / instruction_hiding | 335 | 15 | 4.5% | [2.7%, 7.3%] |
| D0 + D1 / language_switch | 335 | 50 | 14.9% | [11.5%, 19.1%] |
| D0 + D1 / payload_splitting | 330 | 33 | 10.0% | [7.2%, 13.7%] |
| D0 + D1 / role_play | 330 | 23 | 7.0% | [4.7%, 10.2%] |
| D0 + D2 / base | 90 | 0 | 0.0% | [0.0%, 4.1%] |
| D0 + D2 / delimiter_confusion | 85 | 0 | 0.0% | [0.0%, 4.3%] |
| D0 + D2 / encoding_base64 | 87 | 0 | 0.0% | [0.0%, 4.2%] |
| D0 + D2 / encoding_rot13 | 85 | 0 | 0.0% | [0.0%, 4.3%] |
| D0 + D2 / instruction_hiding | 90 | 0 | 0.0% | [0.0%, 4.1%] |
| D0 + D2 / language_switch | 85 | 0 | 0.0% | [0.0%, 4.3%] |
| D0 + D2 / payload_splitting | 85 | 0 | 0.0% | [0.0%, 4.3%] |
| D0 + D2 / role_play | 85 | 0 | 0.0% | [0.0%, 4.3%] |
| D0 + D3 / base | 25 | 0 | 0.0% | [0.0%, 13.3%] |
| D0 + D3 / delimiter_confusion | 20 | 0 | 0.0% | [0.0%, 16.1%] |
| D0 + D3 / encoding_base64 | 22 | 0 | 0.0% | [0.0%, 14.9%] |
| D0 + D3 / encoding_rot13 | 24 | 0 | 0.0% | [0.0%, 13.8%] |
| D0 + D3 / instruction_hiding | 25 | 0 | 0.0% | [0.0%, 13.3%] |
| D0 + D3 / language_switch | 20 | 0 | 0.0% | [0.0%, 16.1%] |
| D0 + D3 / payload_splitting | 20 | 0 | 0.0% | [0.0%, 16.1%] |
| D0 + D3 / role_play | 20 | 0 | 0.0% | [0.0%, 16.1%] |
| D0 + D4 / base | 34 | 0 | 0.0% | [0.0%, 10.2%] |
| D0 + D4 / delimiter_confusion | 29 | 0 | 0.0% | [0.0%, 11.7%] |
| D0 + D4 / encoding_base64 | 33 | 0 | 0.0% | [0.0%, 10.4%] |
| D0 + D4 / encoding_rot13 | 33 | 0 | 0.0% | [0.0%, 10.4%] |
| D0 + D4 / instruction_hiding | 34 | 0 | 0.0% | [0.0%, 10.2%] |
| D0 + D4 / language_switch | 33 | 0 | 0.0% | [0.0%, 10.4%] |
| D0 + D4 / payload_splitting | 29 | 0 | 0.0% | [0.0%, 11.7%] |
| D0 + D4 / role_play | 29 | 0 | 0.0% | [0.0%, 11.7%] |
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
| D0 + D7 / base | 8 | 3 | 37.5% | [13.7%, 69.4%] |
| D0 + D7 / delimiter_confusion | 8 | 0 | 0.0% | [0.0%, 32.4%] |
| D0 + D7 / encoding_base64 | 8 | 0 | 0.0% | [0.0%, 32.4%] |
| D0 + D7 / encoding_rot13 | 8 | 0 | 0.0% | [0.0%, 32.4%] |
| D0 + D7 / instruction_hiding | 8 | 1 | 12.5% | [2.2%, 47.1%] |
| D0 + D7 / language_switch | 8 | 2 | 25.0% | [7.1%, 59.1%] |
| D0 + D7 / payload_splitting | 8 | 0 | 0.0% | [0.0%, 32.4%] |
| D0 + D7 / role_play | 8 | 0 | 0.0% | [0.0%, 32.4%] |
| D0 / base | 354 | 45 | 12.7% | [9.6%, 16.6%] |
| D0 / delimiter_confusion | 355 | 24 | 6.8% | [4.6%, 9.9%] |
| D0 / encoding_base64 | 354 | 0 | 0.0% | [0.0%, 1.1%] |
| D0 / encoding_rot13 | 355 | 0 | 0.0% | [0.0%, 1.1%] |
| D0 / instruction_hiding | 355 | 25 | 7.0% | [4.8%, 10.2%] |
| D0 / language_switch | 355 | 50 | 14.1% | [10.8%, 18.1%] |
| D0 / payload_splitting | 359 | 54 | 15.0% | [11.7%, 19.1%] |
| D0 / role_play | 350 | 26 | 7.4% | [5.1%, 10.7%] |

## Benign utility and blocking false positives

| Defense stack | n | Successful tasks | Success rate | Wilson 95% CI | Blocked benign / FPR | Mean seconds | Mean tokens |
|---|---:|---:|---:|---:|---:|
| D0 | 20 | 5 | 25.0% | [11.2%, 46.9%] | 0/20 (0.0%) | 2.51 | 615.8 |
| D0 + D1 | 95 | 26 | 27.4% | [19.4%, 37.1%] | 0/95 (0.0%) | 5.27 | 689.1 |
| D0 + D2 | 100 | 51 | 51.0% | [41.3%, 60.6%] | 0/100 (0.0%) | 2.53 | 460.2 |
| D0 + D2 + D7 | 20 | 9 | 45.0% | [25.8%, 65.8%] | 0/20 (0.0%) | 3.73 | 466.7 |
| D0 + D3 | 20 | 6 | 30.0% | [14.5%, 51.9%] | 0/20 (0.0%) | 2.21 | 647.1 |
| D0 + D4 | 20 | 5 | 25.0% | [11.2%, 46.9%] | 0/20 (0.0%) | 2.34 | 617.8 |
| D0 + D5 | 20 | 7 | 35.0% | [18.1%, 56.7%] | 0/20 (0.0%) | 2.26 | 669.9 |
| D0 + D6 | 20 | 5 | 25.0% | [11.2%, 46.9%] | 0/20 (0.0%) | 2.31 | 615.9 |
| D0 + D7 | 20 | 5 | 25.0% | [11.2%, 46.9%] | 0/20 (0.0%) | 3.33 | 626.6 |

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
| adb94f2e323040a49f548507f26f2db6 | attack | ollama / llama3.1:8b | D0 | 42 | 5 |
| 76e0aa3e3f4240fb96cde718581a9dd0 | attack | ollama / llama3.1:8b | D0 + D1 | 42 | 5 |
| 5135f71cc2e640549da9016727f2201e | attack | ollama / llama3.1:8b | D0 + D2 | 42 | 5 |
| b10156d78b8d4976a75eb6dc3e27b8d5 | attack | ollama / llama3.1:8b | D0 + D3 | 42 | 5 |
| d545a7dc3dde4cc18f34f4e94543f96c | attack | ollama / llama3.1:8b | D0 + D4 | 42 | 5 |
| df2826d624a44f12ad0f3af780705237 | attack | ollama / llama3.1:8b | D0 | 42 | 5 |
| a3733c3ade0b44a79765921c765fe05c | attack | ollama / llama3.1:8b | D0 | 42 | 5 |
| 5e0a3f58acbd40728a1e5e952be1cb79 | benign | ollama / llama3.1:8b | D0 | 42 | 5 |
| 3bed030dcf3d4c049672ff20a0ece06c | benign | ollama / llama3.1:8b | D0 | 42 | 5 |
| dee73ab754f34e27b3067288382b6c36 | attack | ollama / llama3.1:8b | D0 + D1 | 42 | 5 |
| 9bc5cee207b641188681088e96347de0 | benign | ollama / llama3.1:8b | D0 + D1 | 42 | 5 |
| 178f2f8e93274c1e85087c60d17065ad | attack | ollama / llama3.1:8b | D0 + D2 | 42 | 5 |
| fe9bac87882c4ee1995009ee0392ddf8 | attack | ollama / llama3.1:8b | D0 + D1 | 42 | 5 |
| b35ab22856a94467866d7deed40ffc34 | benign | ollama / llama3.1:8b | D0 + D1 | 42 | 5 |
| cd0ba9deeb82457a90f96cfdb0928d92 | attack | ollama / llama3.1:8b | D0 | 42 | 5 |
| 19fd28aa8978487e88d6399adcfd4ad6 | benign | ollama / llama3.1:8b | D0 + D2 | 42 | 5 |
| 5b1b8b563fe64d0682bee1c57c003872 | attack | ollama / llama3.1:8b | D0 + D3 | 42 | 5 |
| adfeb08a85014dcd9c0476fb84e026e6 | attack | ollama / llama3.1:8b | D0 + D7 | 42 | 1 |
| 14076b1bb91f48c192cd9e4544fcb772 | attack | ollama / llama3.1:8b | D0 + D7 | 42 | 1 |
| 8d5c9c4f18664f53b743198242115cc2 | attack | ollama / llama3.1:8b | D0 + D7 | 42 | 1 |
| 101bb60209124a0daea915bc31d4c2c6 | attack | ollama / llama3.1:8b | D0 + D1 + D2 + D3 + D4 + D5 + D6 + D7 | 42 | 1 |
| 073c0f8e360544539918aa01a24c5b73 | attack | ollama / llama3.1:8b | D0 + D7 | 42 | 1 |
| 3b7ea973aee24b5fa21b5a7d2c31a308 | attack | ollama / llama3.1:8b | D0 + D1 + D2 + D3 + D4 + D5 + D6 + D7 | 42 | 1 |
| dc8908a27d6e4e9f94e50c33381b8c72 | attack | ollama / llama3.1:8b | D0 + D7 | 42 | 1 |
| 292689a588a64f64bfa88053e01f0b7c | benign | ollama / llama3.1:8b | D0 + D7 | 42 | 1 |
| 2321932886e44e4bb32f9daaf5f4630f | benign | ollama / llama3.1:8b | D0 + D2 + D7 | 42 | 1 |
| 7be19efdef6b4b90ae0f8c43140d9876 | attack | ollama / llama3.1:8b | D0 | 42 | 5 |
| 5a387663a70e428f960fe25a7eb13100 | attack | ollama / llama3.1:8b | D0 + D7 | 42 | 1 |
| 999518cae8b64d9db0a781c7b77f8ff4 | benign | ollama / llama3.1:8b | D0 + D7 | 42 | 1 |
| 1675510fa3054cda834615799f524226 | benign | ollama / llama3.1:8b | D0 + D7 | 42 | 1 |
| 259d2f6719454c758d7a876adf097749 | benign | ollama / llama3.1:8b | D0 + D7 | 42 | 1 |
| f90ea6dafb17481c9cdac73c4b61b4dc | benign | ollama / llama3.1:8b | D0 + D7 | 42 | 1 |
| 5e3a6b8275914d8ca9cd10b13e3143ca | benign | ollama / llama3.1:8b | D0 + D2 + D7 | 42 | 1 |
| cb6b9195fe1d43d7ba9183c7b2881642 | attack | ollama / llama3.1:8b | D0 | 42 | 5 |
| dffbce5dab5c4a6ebd9d3fc6c67dc391 | attack | ollama / llama3.1:8b | D0 | 42 | 5 |
| cc7f1dcfffea4a20bb6e43bfdf650809 | attack | ollama / llama3.1:8b | D0 | 42 | 5 |
| cde0424c42d24c539cc13e603a2649fe | attack | ollama / llama3.1:8b | D0 | 42 | 1 |
| 87596c56520a4276ab65afe02f735e9b | attack | ollama / llama3.1:8b | D0 | 42 | 5 |
| 805513f09e0d4cf99797f9dbdf1393b3 | attack | ollama / llama3.1:8b | D0 + D7 | 42 | 1 |
| a59d8760ccca4dc689980cba0055e7e2 | attack | ollama / llama3.1:8b | D0 + D1 + D2 + D3 + D4 + D5 + D6 + D7 | 42 | 1 |

## Limitations and what did not work

- D5 context-isolation model overhead has not been measured in saved runs.
- The current evaluator is deterministic and uses declared trace criteria; no LLM judge labels are included. Human calibration remains pending paired annotations.
- Local Ollama timings and behavior are specific to the recorded model, machine, temperature, and seeds. The mock email tool writes only to its local in-memory outbox.

## Reproduction

Use `agentsec reproduce` with the same backend and model configuration to run the default full ablation. Each trial is committed to SQLite as it completes; rerunning with the same database resumes missing or errored cases. `agentsec report` rebuilds this document and the SVG using saved data only.

Sources: [OWASP GenAI LLM Top 10 (2026)](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/); [NIST AI RMF Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf).
