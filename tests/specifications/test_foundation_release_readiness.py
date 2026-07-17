from pathlib import Path


REQUIRED_FOUNDATION_DOCUMENTS = (
    "research/releases/HAS_FOUNDATION_1_0_RELEASE_CONTRACT.md",
)

REQUIRED_SPECIFICATION_DOCUMENTS = (
    "research/specifications/runtime_specification.md",
    "research/specifications/RELEASE_GATES.md",
    "research/specifications/SPECIFICATION_GRAMMAR.md",
    "research/specifications/SPECIFICATION_STYLE_GUIDE.md",
)

REQUIRED_CONFORMANCE_DOCUMENTS = (
    "research/conformance/CONFORMANCE_INPUT_CONTRACT.md",
    "research/conformance/CONFORMANCE_DECISION_MODEL.md",
    "research/conformance/CONFORMANCE_EVIDENCE_MODEL.md",
    "research/conformance/CONFORMANCE_EVALUATOR_CONTRACT.md",
    "research/conformance/CONFORMANCE_DECISION_RECORD.md",
)

REQUIRED_CLOSE_AUDITS = (
    "tests/specifications/test_eki_close_001.py",
    "tests/specifications/test_sp_audit_001.py",
    "tests/specifications/test_conf_close_001.py",
)


def test_foundation_release_contract_exists() -> None:
    for path in REQUIRED_FOUNDATION_DOCUMENTS:
        assert Path(path).is_file()


def test_specification_platform_is_complete() -> None:
    for path in REQUIRED_SPECIFICATION_DOCUMENTS:
        assert Path(path).is_file()


def test_conformance_platform_is_complete() -> None:
    for path in REQUIRED_CONFORMANCE_DOCUMENTS:
        assert Path(path).is_file()


def test_foundation_close_audits_exist() -> None:
    for path in REQUIRED_CLOSE_AUDITS:
        assert Path(path).is_file()
