from collections import Counter

from agentsec.attacks.library import load_attack_library, load_base_attacks
from agentsec.attacks.schema import AttackCategory, CriterionOperator, MutationType


def test_base_corpus_has_ten_valid_attacks_per_category() -> None:
    attacks = load_base_attacks()
    counts = Counter(attack.category for attack in attacks)
    assert len(attacks) == 80
    assert set(counts) == set(AttackCategory)
    assert all(counts[category] >= 10 for category in AttackCategory)
    assert all(attack.success_criteria for attack in attacks)


def test_default_mutation_expansion_exceeds_150_and_tracks_sources() -> None:
    attacks = load_attack_library()
    base = [attack for attack in attacks if attack.mutation_type == MutationType.BASE]
    assert len(attacks) == 640
    assert len(base) == 80
    assert all(
        attack.base_attack_id for attack in attacks if attack.mutation_type != MutationType.BASE
    )
    generated_types = {attack.mutation_type for attack in attacks}
    assert generated_types >= set(MutationType) - {MutationType.PARAPHRASE}
    split = next(
        attack for attack in attacks if attack.mutation_type == MutationType.PAYLOAD_SPLITTING
    )
    assert len(split.payload_fragments) == 2
    assert split.payload_fragments[0].order == 0
    assert split.payload_fragments[1].order == 1


def test_data_exfiltration_criterion_is_machine_checkable() -> None:
    attack = next(
        attack
        for attack in load_base_attacks()
        if attack.category == AttackCategory.DATA_EXFILTRATION
    )
    criterion = attack.success_criteria[0]
    assert criterion.operator == CriterionOperator.CONTAINS
    assert criterion.matches(
        {
            "event_type": "tool_call",
            "data": {"arguments": {"body": "The fake value is CANARY-4F2A"}},
        }
    )
    assert not criterion.matches(
        {"event_type": "tool_call", "data": {"arguments": {"body": "No secret"}}}
    )


def test_llm_paraphraser_is_optional_and_labeled() -> None:
    attacks = load_base_attacks()[:1]
    expanded = load_attack_library(include_mutations=False)
    assert len(expanded) == 80
    from agentsec.attacks.mutations import MutationEngine

    variants = MutationEngine().expand(attacks, paraphraser=lambda text: f"Paraphrased: {text}")
    paraphrase = next(item for item in variants if item.mutation_type == MutationType.PARAPHRASE)
    assert paraphrase.base_attack_id == attacks[0].id
    assert paraphrase.payload.startswith("Paraphrased:")
