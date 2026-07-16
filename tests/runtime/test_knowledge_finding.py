from has.runtime.knowledge_finding import (
    KnowledgeFinding,
)


def test_finding():

    finding = KnowledgeFinding(
        code="HAS-001",
        message="History is discontinuous",
        severity="error",
    )

    assert finding.code == "HAS-001"

    assert (
        finding.message
        == "History is discontinuous"
    )

    assert finding.severity == "error"
