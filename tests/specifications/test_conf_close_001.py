from pathlib import Path


REQUIRED_RUNTIME = (
    "src/has/conformance/conformance_pipeline.py",
    "src/has/conformance/decision_evaluator.py",
)

REQUIRED_MODELS = (
    "src/has/conformance/model/conformance_input.py",
    "src/has/conformance/model/evidence.py",
    "src/has/conformance/model/decision.py",
    "src/has/conformance/model/decision_record.py",
)

REQUIRED_POLICIES = (
    "src/has/conformance/policies/decision_policy.py",
    "src/has/conformance/policies/covered_policy.py",
)

REQUIRED_SPECIFICATIONS = (
    "research/conformance/CONFORMANCE_INPUT_CONTRACT.md",
    "research/conformance/CONFORMANCE_DECISION_MODEL.md",
    "research/conformance/CONFORMANCE_EVIDENCE_MODEL.md",
    "research/conformance/CONFORMANCE_EVALUATOR_CONTRACT.md",
    "research/conformance/CONFORMANCE_DECISION_RECORD.md",
)


def test_runtime_components_exist() -> None:
    for path in REQUIRED_RUNTIME:
        assert Path(path).is_file()


def test_domain_models_exist() -> None:
    for path in REQUIRED_MODELS:
        assert Path(path).is_file()


def test_policy_layer_exists() -> None:
    for path in REQUIRED_POLICIES:
        assert Path(path).is_file()


def test_normative_documents_exist() -> None:
    for path in REQUIRED_SPECIFICATIONS:
        assert Path(path).is_file()
