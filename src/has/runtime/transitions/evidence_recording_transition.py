from has.runtime.evidence_accumulator import EvidenceAccumulator
from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.transitions.knowledge_transition import KnowledgeTransition


class EvidenceRecordingTransition(KnowledgeTransition):
    """Records evidence without changing knowledge state."""

    def __init__(
        self,
        accumulator: EvidenceAccumulator,
    ) -> None:
        self._accumulator = accumulator

    def execute(
        self,
        artifact: KnowledgeArtifact,
    ) -> KnowledgeArtifact:
        return self._accumulator.record(artifact)
