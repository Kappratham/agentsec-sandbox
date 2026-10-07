# Attack library

`base_attacks.json` contains 80 hand-authored base cases: 10 in each of the eight supported categories. `agentsec attacks validate` validates the source and expands it into deterministic variants. The default expansion yields one base plus seven mutations for every base case. The optional LLM paraphraser is an injected callback and is not invoked by the default command.

Each expanded record is validated by Pydantic. Success conditions use a small safe predicate schema (`event_type`, dotted `field`, `operator`, and `value`); they do not execute expressions. Mutations preserve the base record ID and label their transformation. Split-payload variants record each fragment and source channel.

## Framework mappings

The OWASP mapping uses the current 2026 release. OWASP renamed and reordered categories between editions, so IDs include the year and should not be compared to older numbering without a crosswalk. Each attack maps to one or more OWASP risk areas. The NIST values refer to risk areas in the Generative AI Profile companion to AI RMF 1.0; these are analyst-selected relationships, not official one-to-one attack categories.

- [OWASP GenAI LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/)
- [NIST AI RMF Generative AI Profile (NIST AI 600-1)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [NIST AI RMF status and resources](https://www.nist.gov/itl/ai-risk-management-framework)
