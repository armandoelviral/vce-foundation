from sp001.models.capability_candidate import CapabilityCandidate
from sp001.models.case import Case
from sp001.models.expert_decision import ExpertDecision
from sp001.models.institutional_capability import InstitutionalCapability
from sp001.models.objective import Objective
from sp001.models.operational_evidence import OperationalEvidence
from sp001.models.recommendation import Recommendation


def test_scientific_product_language_exists() -> None:
    assert Objective is not None
    assert Case is not None
    assert Recommendation is not None
    assert ExpertDecision is not None
    assert OperationalEvidence is not None
    assert CapabilityCandidate is not None
    assert InstitutionalCapability is not None
