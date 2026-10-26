from dataclasses import dataclass

from sp001.contracts.knowledge_source_identity import KnowledgeSourceIdentity


@dataclass(frozen=True, slots=True)
class EvidenceFileExpectation:
    """Declared source identity and expected length; establishes no authority."""

    identity: KnowledgeSourceIdentity
    byte_length: int

    def __post_init__(self):
        if not isinstance(self.identity, KnowledgeSourceIdentity):
            raise TypeError("identity must be a KnowledgeSourceIdentity")
        if type(self.byte_length) is not int:
            raise TypeError("byte_length must be an integer")
        if self.byte_length < 1:
            raise ValueError("byte_length must be positive")
