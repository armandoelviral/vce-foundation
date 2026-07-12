from sp001.models.operational_evidence import OperationalEvidence
from sp001.models.capability_candidate import CapabilityCandidate


def test_operational_evidence_creates_capability_candidate() -> None:
    evidence = OperationalEvidence()

    candidate = evidence.create_capability_candidate()

    assert isinstance(candidate, CapabilityCandidate)
