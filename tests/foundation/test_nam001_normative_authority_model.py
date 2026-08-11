from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]

MODEL = (
    ROOT
    / "research"
    / "foundation"
    / "normative_authority"
    / "NAM001_NORMATIVE_AUTHORITY_MODEL.md"
)

FREEZE = (
    ROOT
    / "research"
    / "foundation"
    / "normative_authority"
    / "NAM001_AUTHORITY_MODEL_FREEZE.md"
)

CYCLE_1 = (
    ROOT
    / "research"
    / "foundation"
    / "normative_authority"
    / "NAM001_REFUTATION_CYCLE_1.md"
)

CYCLE_2 = (
    ROOT
    / "research"
    / "foundation"
    / "normative_authority"
    / "NAM001_REFUTATION_CYCLE_2_ADVERSARIAL.md"
)

CYCLE_3 = (
    ROOT
    / "research"
    / "foundation"
    / "normative_authority"
    / "NAM001_REFUTATION_CYCLE_3_MINIMALITY_DETERMINISM_REPLAY.md"
)

CYCLE_4 = (
    ROOT
    / "research"
    / "foundation"
    / "normative_authority"
    / "NAM001_REFUTATION_CYCLE_4_FINAL_ADVERSARIAL.md"
)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(content: str) -> str:
    return " ".join(content.split())


def model_text() -> str:
    return text(MODEL)


def freeze_text() -> str:
    return text(FREEZE)


def section(content: str, start: str, end: str) -> str:
    return content[
        content.index(start):
        content.index(end)
    ]


def enum_values(content: str, start: str, end: str) -> list[str]:
    block = section(content, start, end)

    return re.findall(
        r"^([A-Z][A-Z_]+)\.$",
        block,
        flags=re.MULTILINE,
    )


def test_required_nam001_artifacts_exist() -> None:
    for path in (
        MODEL,
        FREEZE,
        CYCLE_1,
        CYCLE_2,
        CYCLE_3,
        CYCLE_4,
    ):
        assert path.is_file(), f"missing NAM-001 artifact: {path}"


def test_nam001_identity() -> None:
    content = normalized(model_text())

    assert "Identifier NAM-001" in content
    assert "Version 1.0" in content
    assert "Status Normative" in content
    assert "Normative Authority Baseline" in content


def test_nam001_declares_promoted_authority() -> None:
    content = normalized(model_text())

    assert "Baseline 1.0" in content
    assert "Authority AUTHORITATIVE." in content
    assert (
        "Authority Scope Normative authority representation, "
        "evaluation, transition, and replay."
        in content
    )
    assert "Promotion Gate PASSED." in content
    assert "Freeze ACTIVE." in content


def test_nam001_preserves_promoted_source_identity() -> None:
    content = normalized(model_text())

    assert "Source Candidate NAM-001 Version 0.4." in content


def test_nam001_does_not_self_authorize() -> None:
    content = normalized(model_text())

    assert "NAM-001 does not grant authority to itself." in content
    assert "NAM-001 does not grant authority to any other artifact." in content


def test_authority_is_not_inferred_from_repository_accident() -> None:
    content = normalized(model_text())

    forbidden_sources = (
        "File presence.",
        "Repository path.",
        "Directory depth.",
        "Version recency.",
        "Commit order.",
        "Tag presence.",
        "Implementation behavior.",
        "Test behavior.",
        "Execution order.",
        "Dependency direction.",
        "Reference count.",
        "Historical popularity.",
        "Naming convention.",
        "Architectural importance.",
        "Commercial importance.",
    )

    for item in forbidden_sources:
        assert item in content


def test_relationship_identity_is_stable() -> None:
    content = normalized(model_text())

    assert "Every authority relationship shall possess stable identity." in content
    assert "A material change to normative identity shall require a new Relationship Identifier." in content


def test_identity_materiality_requires_new_identity_for_core_changes() -> None:
    content = normalized(model_text())

    for change in (
        "Authority Source change.",
        "Repository Authority Context change.",
        "Fundamental Relationship Type change.",
        "Fundamental Authority Target change.",
    ):
        assert change in content


def test_nam001_declares_exactly_ten_relationship_types() -> None:
    values = enum_values(
        model_text(),
        "## Authority Relationship Types",
        "## Direct Authority",
    )

    expected = [
        "DIRECT_AUTHORITY",
        "DERIVED_AUTHORITY",
        "DELEGATED_AUTHORITY",
        "TRANSFERRED_AUTHORITY",
        "CLASSIFICATION_AUTHORITY",
        "LIFECYCLE_AUTHORITY",
        "PROMOTION_AUTHORITY",
        "CONFLICT_RESOLUTION_AUTHORITY",
        "JOINT_AUTHORITY",
        "SUBORDINATION",
    ]

    assert values == expected


def test_quorum_is_not_an_independent_relationship_type() -> None:
    content = normalized(model_text())

    assert (
        "A quorum shall be represented as a Joint Authority "
        "configuration with a threshold rule."
        in content
    )

    relationship_values = enum_values(
        model_text(),
        "## Authority Relationship Types",
        "## Direct Authority",
    )

    assert "QUORUM_AUTHORITY" not in relationship_values


def test_classification_authority_does_not_grant_candidate_authority() -> None:
    content = normalized(model_text())

    assert (
        "Classification Authority shall not grant normative authority "
        "to classified candidates."
        in content
    )


def test_lifecycle_authority_does_not_become_semantic_authority() -> None:
    content = normalized(model_text())

    assert (
        "Lifecycle Authority shall not automatically create semantic authority "
        "over governed artifacts."
        in content
    )


def test_promotion_authority_requires_traceable_authorization() -> None:
    content = normalized(model_text())

    assert (
        "A Promotion Gate shall not possess Promotion Authority "
        "merely because it uses that name."
        in content
    )


def test_subordination_is_scope_bounded() -> None:
    content = normalized(model_text())

    assert (
        "Subordination shall not imply universal superiority "
        "outside that scope."
        in content
    )


def test_nam001_declares_exactly_five_dispositions() -> None:
    values = enum_values(
        model_text(),
        "## Authority Disposition",
        "## Effectivity",
    )

    assert values == [
        "ESTABLISHED",
        "SUSPENDED",
        "SUPERSEDED",
        "WITHDRAWN",
        "INVALIDATED",
    ]


def test_disposition_does_not_encode_other_dimensions() -> None:
    content = normalized(model_text())

    assert "Disposition shall not encode:" in content
    assert "Candidate lifecycle state." in content
    assert "Effectivity." in content
    assert "Applicability." in content
    assert "Historical perspective." in content


def test_nam001_declares_exactly_four_effectivity_values() -> None:
    values = enum_values(
        model_text(),
        "## Effectivity",
        "## Applicability",
    )

    assert values == [
        "EFFECTIVE",
        "NOT_YET_EFFECTIVE",
        "EXPIRED",
        "TERMINATED",
    ]


def test_nam001_declares_exactly_three_applicability_values() -> None:
    values = enum_values(
        model_text(),
        "## Applicability",
        "## Candidate Status",
    )

    assert values == [
        "APPLICABLE",
        "NOT_APPLICABLE",
        "UNRESOLVED_APPLICABILITY",
    ]


def test_effectivity_and_applicability_are_distinct() -> None:
    content = normalized(model_text())

    assert "Applicability shall remain distinct from Effectivity." in content


def test_candidate_status_is_not_authority_disposition() -> None:
    content = normalized(model_text())

    assert (
        "Candidate status shall remain outside normative authority disposition."
        in content
    )


def test_historical_is_not_an_authority_disposition() -> None:
    content = normalized(model_text())

    assert "HISTORICAL shall not be modeled as a disposition." in content


def test_evaluation_time_is_pinned() -> None:
    content = normalized(model_text())

    assert "Every authority evaluation shall pin an Evaluation Time." in content
    assert (
        "Evaluation Time shall not change during one authority projection "
        "or replay operation."
        in content
    )


def test_temporal_interval_boundaries_are_explicit() -> None:
    content = normalized(model_text())

    assert "Effective Start shall be inclusive." in content
    assert "Effective End shall be exclusive." in content
    assert "An absent Effective End shall represent an open interval." in content


def test_zero_length_interval_has_no_default_authority() -> None:
    content = normalized(model_text())

    assert (
        "Effective Start equals Effective End, "
        "the relationship shall possess no effective interval"
        in content
    )


def test_ambiguous_conditions_fail_to_unresolved_applicability() -> None:
    content = normalized(model_text())

    assert (
        "Missing or ambiguous required condition evidence shall produce: "
        "UNRESOLVED_APPLICABILITY."
        in content
    )


def test_authority_changes_require_transition_records() -> None:
    content = normalized(model_text())

    assert (
        "Authority changes shall be represented through explicit "
        "transition records."
        in content
    )

    assert (
        "Direct destructive mutation shall not replace "
        "historical transition evidence."
        in content
    )


def test_nam001_declares_exactly_twelve_transition_types() -> None:
    values = enum_values(
        model_text(),
        "## Transition Types",
        "## Derived Expiration",
    )

    assert values == [
        "ESTABLISH",
        "SUSPEND",
        "REACTIVATE",
        "SUPERSEDE",
        "WITHDRAW",
        "INVALIDATE",
        "DELEGATE",
        "TRANSFER",
        "REVOKE",
        "AMEND_SCOPE",
        "AMEND_CONDITION",
        "AMEND_INTERVAL",
    ]


def test_expiration_is_derived_not_top_level_transition() -> None:
    content = normalized(model_text())

    transitions = enum_values(
        model_text(),
        "## Transition Types",
        "## Derived Expiration",
    )

    assert "EXPIRE" not in transitions

    assert (
        "Expiration shall be derived from: "
        "Effective End. Evaluation Time."
        in content
    )


def test_root_transitions_use_general_transition_types() -> None:
    content = normalized(model_text())

    assert "Separate ROOT_SUSPEND, ROOT_INVALIDATE, and ROOT_REPLACE" in content
    assert "shall not be required." in content


def test_terminal_dispositions_are_explicit() -> None:
    content = normalized(model_text())

    for disposition in (
        "SUPERSEDED.",
        "WITHDRAWN.",
        "INVALIDATED.",
    ):
        assert disposition in content

    assert (
        "A terminal relationship shall not silently return to ESTABLISHED."
        in content
    )


def test_suspension_is_reactivatable() -> None:
    content = normalized(model_text())

    assert (
        "A suspended relationship shall return to ESTABLISHED "
        "only through an authorized REACTIVATE transition"
        in content
    )


def test_retroactivity_is_explicit_not_default() -> None:
    content = normalized(model_text())

    assert "Authority transitions shall be prospective by default." in content
    assert "Retroactive effect shall require explicit authorization." in content


def test_authority_dependency_is_explicit() -> None:
    content = normalized(model_text())

    assert "Authority dependency shall be explicit." in content
    assert "Graph reachability alone shall not establish dependency." in content


def test_dependency_propagation_is_scope_and_type_aware() -> None:
    content = normalized(model_text())

    assert "Scope-aware." in content
    assert "Type-aware." in content
    assert "Transition-aware." in content


def test_transfer_scope_does_not_expand_authority() -> None:
    content = normalized(model_text())

    assert "Transfer shall operate on explicit scope." in content
    assert "Untransferred scope shall remain unaffected." in content


def test_authority_chain_requires_valid_root() -> None:
    content = normalized(model_text())

    assert (
        "Every current authority chain shall remain traceable "
        "to at least one valid Authority Root"
        in content
    )


def test_multiple_roots_are_permitted() -> None:
    content = normalized(model_text())

    assert "Multiple roots may exist." in content
    assert (
        "No universal repository-independent root shall be assumed."
        in content
    )


def test_authority_granting_mechanisms_cannot_self_authorize() -> None:
    content = normalized(model_text())

    assert "Authority-granting mechanisms shall not self-authorize." in content


def test_circular_support_cannot_create_authority() -> None:
    content = normalized(model_text())

    assert "Authority is created solely through circular support." in content
    assert "independently valid authority root" in content.lower()
    assert "can be reached" in content.lower()


def test_root_failure_requires_dependency_evaluation() -> None:
    content = normalized(model_text())

    assert (
        "shall trigger explicit dependency evaluation."
        in content
    )

    assert "Current validity." in content
    assert "Historical validity." in content
    assert "Retroactive validity." in content


def test_root_compromise_does_not_invent_precise_time() -> None:
    content = normalized(model_text())

    assert (
        "Uncertain compromise time shall remain uncertain."
        in content
    )

    assert (
        "It shall not be silently converted to a precise historical boundary."
        in content
    )


def test_joint_authority_configuration_is_pinned() -> None:
    content = normalized(model_text())

    assert (
        "Joint Authority shall use a pinned Authority Configuration."
        in content
    )

    assert "Configuration Identifier." in content
    assert "Membership Set." in content
    assert "Required Participation or Threshold." in content
    assert "Decision Rule." in content


def test_configuration_changes_do_not_change_in_progress_decision() -> None:
    content = normalized(model_text())

    assert "Membership," in content
    assert "threshold," in content
    assert "decision-rule changes" in content
    assert "shall not alter" in content
    assert "pinned" in content
    assert "configuration" in content


def test_authority_conflict_requires_effective_and_applicable_authority() -> None:
    content = normalized(model_text())

    assert (
        "Authority conflict exists when two simultaneously: "
        "EFFECTIVE. APPLICABLE. authority relationships"
        in content
    )


def test_authority_precedence_is_not_implicit() -> None:
    content = normalized(model_text())

    forbidden = (
        "Identifier.",
        "File location.",
        "Repository path.",
        "Version number.",
        "Recency.",
        "Specificity.",
        "Implementation adoption.",
        "Test coverage.",
        "Reference count.",
        "Commercial importance.",
    )

    for item in forbidden:
        assert item in content


def test_transition_conflict_does_not_use_file_order() -> None:
    content = normalized(model_text())

    assert "File order shall not resolve the conflict." in content
    assert "authority evaluation shall become: UNRESOLVED." in content


def test_authority_evaluation_is_deterministic() -> None:
    content = normalized(model_text())

    assert "## Deterministic Evaluation" in model_text()

    assert (
        "an evaluator shall produce the same: "
        "Effective Authority Projection. "
        "or explicit unresolved result."
        in content
    )


def test_determinism_rejects_wall_clock_and_iteration_order() -> None:
    content = normalized(model_text())

    assert "File order." in content
    assert "Iteration order." in content
    assert "Wall-clock drift." in content
    assert "Implementation-specific collection ordering." in content


def test_evaluation_must_terminate() -> None:
    content = normalized(model_text())

    assert "Authority evaluation shall terminate." in content
    assert "Cycles shall not produce unbounded recursion." in content


def test_missing_authority_evidence_fails_closed() -> None:
    content = normalized(model_text())

    assert "Authority evaluation shall not invent missing authority evidence." in content
    assert "Authority shall not be assumed." in content


def test_fail_closed_lists_required_evidence_classes() -> None:
    content = normalized(model_text())

    for item in (
        "Authority Source.",
        "Transition History.",
        "Historical Conditions.",
        "Configuration Snapshot.",
        "Dependency Evidence.",
        "Conflict Rule.",
        "Root Evidence.",
    ):
        assert item in content


def test_effective_projection_requires_all_authority_conditions() -> None:
    content = normalized(model_text())

    requirements = (
        "Disposition permits authority.",
        "Effectivity is EFFECTIVE.",
        "Applicability is APPLICABLE.",
        "Dependencies are satisfied.",
        "Required root authority is valid.",
        "No unresolved blocking conflict exists.",
    )

    for requirement in requirements:
        assert requirement in content


def test_authority_replay_pins_inputs() -> None:
    content = normalized(model_text())

    for item in (
        "Repository Authority Context.",
        "Scope.",
        "Evaluation Time.",
        "Replay Mode.",
        "Historical Conditions.",
        "Authority Configuration.",
        "Authority Evidence Set.",
        "Transition Evidence Set.",
        "Root Evidence Set.",
    ):
        assert item in content


def test_nam001_declares_exactly_two_replay_modes() -> None:
    values = enum_values(
        model_text(),
        "## Replay Modes",
        "## Knowledge-at-Time Replay",
    )

    assert values == [
        "KNOWLEDGE_AT_TIME",
        "RETROSPECTIVE_AUTHORITY",
    ]


def test_knowledge_at_time_excludes_future_evidence() -> None:
    content = normalized(model_text())

    assert (
        "Later evidence shall not be silently injected."
        in content
    )


def test_retrospective_replay_supports_authorized_retroactivity() -> None:
    content = normalized(model_text())

    assert (
        "RETROSPECTIVE_AUTHORITY shall reconstruct "
        "what authority is currently considered to have governed"
        in content
    )

    assert (
        "after applying authorized retroactive authority transitions."
        in content
    )


def test_replay_is_deterministic() -> None:
    content = normalized(model_text())

    assert (
        "Given identical replay inputs, authority replay shall produce "
        "the same authority result or the same explicit unresolved result."
        in content
    )


def test_missing_historical_configuration_is_not_replaced_by_current() -> None:
    content = normalized(model_text())

    assert (
        "Historical gaps shall not be filled using "
        "current configuration or assumption."
        in content
    )


def test_duplicate_relationship_identity_is_not_parallel_authority() -> None:
    content = normalized(model_text())

    assert (
        "Duplicate identity shall not silently create parallel authority."
        in content
    )


def test_authority_ambiguity_remains_explicit() -> None:
    content = normalized(model_text())

    assert "Authority ambiguity shall not be resolved through assumption." in content


def test_edge_minimality_excludes_non_authority_relationships() -> None:
    content = normalized(model_text())

    for item in (
        "Import.",
        "Execution order.",
        "File reference.",
        "Test coverage.",
        "Artifact derivation.",
        "Data flow.",
        "Deployment relationship.",
        "Historical association.",
        "Shared implementation.",
        "Documentation reference.",
        "Ordinary software dependency.",
    ):
        assert item in content


def test_executable_contracts_do_not_create_authority() -> None:
    content = normalized(model_text())

    assert (
        "They shall not create authority merely through "
        "execution or successful tests."
        in content
    )


def test_implementation_does_not_create_authority() -> None:
    content = normalized(model_text())

    assert "Implementation shall not create authority through:" in content
    assert "Implementation consensus shall not silently resolve normative ambiguity." in content


def test_evidence_does_not_automatically_create_or_terminate_authority() -> None:
    content = normalized(model_text())

    assert (
        "Evidence shall not automatically create or terminate normative authority."
        in content
    )


def test_freeze_does_not_create_authority() -> None:
    content = normalized(model_text())

    assert "Freeze shall not automatically create authority." in content
    assert "Freeze shall not become an authority layer." in content


def test_nam001_preserves_orthogonal_model_boundary() -> None:
    content = normalized(model_text())

    for model in (
        "Architecture Layer Model.",
        "Runtime Processing Model.",
        "Evidence Processing Model.",
        "Artifact Lifecycle Model.",
        "Deployment Topology.",
        "Repository Directory Model.",
        "Specification Lifecycle.",
    ):
        assert model in content


def test_current_foundation_is_not_collapsed_into_linear_hierarchy() -> None:
    content = normalized(model_text())

    assert "RC-001" in content
    assert "SL-001" in content
    assert "APC-001" in content

    assert (
        "These scopes shall not be collapsed into one universal "
        "linear hierarchy."
        in content
    )


def test_cta_remains_non_authoritative() -> None:
    content = normalized(model_text())

    assert "Common Trust Architecture remains non-authoritative." in content

    assert (
        "Historical use within CP-001 shall not establish CTA authority."
        in content
    )


def test_post_promotion_cta_remains_non_authoritative() -> None:
    content = normalized(model_text())

    assert "Common Trust Architecture NON-AUTHORITATIVE." in content


def test_post_promotion_ap_candidates_remain_non_authoritative() -> None:
    content = normalized(model_text())

    assert "Architecture Principle Candidates NON-AUTHORITATIVE." in content


def test_freeze_identity() -> None:
    content = normalized(freeze_text())

    assert "Identifier NAM-001-FREEZE" in content
    assert "Version 1.0" in content
    assert "Status Active Freeze" in content
    assert "NAM-001 Normative Authority Model Version 0.4" in content


def test_freeze_declares_active_promoted_authority() -> None:
    content = normalized(freeze_text())

    assert "Authority AUTHORITATIVE." in content
    assert (
        "Authority Scope Normative authority representation, "
        "evaluation, transition, and replay."
        in content
    )
    assert "Promotion Gate PASSED." in content
    assert "Freeze ACTIVE." in content


def test_freeze_declares_exactly_ten_relationship_types() -> None:
    content = normalized(freeze_text())

    assert (
        "Exactly ten top-level Authority Relationship Types are frozen."
        in content
    )


def test_freeze_declares_exactly_five_dispositions() -> None:
    content = normalized(freeze_text())

    assert "Exactly five Authority Dispositions are frozen." in content


def test_freeze_declares_exactly_four_effectivity_values() -> None:
    content = normalized(freeze_text())

    assert "Exactly four Effectivity Values are frozen." in content


def test_freeze_declares_exactly_three_applicability_values() -> None:
    content = normalized(freeze_text())

    assert "Exactly three Applicability Values are frozen." in content


def test_freeze_declares_exactly_twelve_transition_types() -> None:
    content = normalized(freeze_text())

    assert (
        "Exactly twelve top-level Transition Types are frozen."
        in content
    )


def test_freeze_declares_exactly_two_replay_modes() -> None:
    content = normalized(freeze_text())

    assert "Exactly two Replay Modes are frozen." in content


def test_freeze_preserves_determinism() -> None:
    content = normalized(freeze_text())

    assert "Frozen Determinism" in content

    assert (
        "an evaluator shall produce the same: "
        "Effective Authority Projection. "
        "or explicit unresolved result."
        in content
    )


def test_freeze_preserves_fail_closed_semantics() -> None:
    content = normalized(freeze_text())

    assert "Frozen Fail-Closed Rule" in content
    assert "Authority shall not be assumed." in content


def test_freeze_preserves_evaluation_termination() -> None:
    content = normalized(freeze_text())

    assert "Frozen Evaluation Termination" in content
    assert "Authority evaluation shall terminate." in content


def test_freeze_preserves_replay_modes() -> None:
    content = normalized(freeze_text())

    assert "KNOWLEDGE_AT_TIME." in content
    assert "RETROSPECTIVE_AUTHORITY." in content


def test_freeze_preserves_authority_of_authority() -> None:
    content = normalized(freeze_text())

    assert "Frozen Authority-of-Authority" in content

    assert (
        "Authority-granting mechanisms shall not self-authorize."
        in content
    )


def test_freeze_preserves_cta_boundary() -> None:
    content = normalized(freeze_text())

    assert "Frozen CTA Boundary" in content
    assert "Common Trust Architecture remains non-authoritative." in content


def test_cycle_1_has_thirty_six_cases() -> None:
    cases = re.findall(
        r"^# AG-(\d{3}) —",
        text(CYCLE_1),
        flags=re.MULTILINE,
    )

    assert cases == [
        f"{i:03d}"
        for i in range(1, 37)
    ]


def test_cycle_2_has_forty_cases() -> None:
    cases = re.findall(
        r"^# ST-(\d{3}) —",
        text(CYCLE_2),
        flags=re.MULTILINE,
    )

    assert cases == [
        f"{i:03d}"
        for i in range(1, 41)
    ]


def test_cycle_3_has_fifty_cases() -> None:
    cases = re.findall(
        r"^# MD-(\d{3}) —",
        text(CYCLE_3),
        flags=re.MULTILINE,
    )

    assert cases == [
        f"{i:03d}"
        for i in range(1, 51)
    ]


def test_cycle_4_has_sixty_cases() -> None:
    cases = re.findall(
        r"^# FD-(\d{3}) —",
        text(CYCLE_4),
        flags=re.MULTILINE,
    )

    assert cases == [
        f"{i:03d}"
        for i in range(1, 61)
    ]


def test_final_cycle_reports_zero_determinism_failures() -> None:
    content = normalized(text(CYCLE_4))

    assert "Cases Evaluated 60." in content
    assert "Determinism Failures 0." in content
    assert "Replay Model Failures 0." in content
    assert "False Authority Grants 0." in content
    assert "Implicit Precedence Failures 0." in content


def test_final_cycle_requires_no_taxonomy_expansion() -> None:
    content = normalized(text(CYCLE_4))

    assert "Required New Relationship Types 0." in content
    assert "Required New Authority Dispositions 0." in content
    assert "Required New Effectivity Values 0." in content
    assert "Required New Applicability Values 0." in content
    assert "Required New Transition Types 0." in content
    assert "Required New Replay Modes 0." in content


def test_final_cycle_declares_freeze_readiness_candidate() -> None:
    content = normalized(text(CYCLE_4))

    assert "Freeze Readiness CANDIDATE." in content
