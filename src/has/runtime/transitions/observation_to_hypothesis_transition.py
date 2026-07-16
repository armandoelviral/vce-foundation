from has.runtime.evaluation_requirements import (
    EvaluationRequirements,
)
from has.runtime.evidence_accumulator import EvidenceAccumulator
from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_evaluator import KnowledgeEvaluator
from has.runtime.knowledge_promoter import KnowledgePromoter
from has.runtime.knowledge_state import KnowledgeState
from has.runtime.transitions.evidence_recording_transition import (
    EvidenceRecordingTransition,
)
from has.runtime.transitions.knowledge_transition import (
    KnowledgeTransition,
)


class ObservationToHypothesisTransition(KnowledgeTransition):
    """Records evidence, evaluates readiness, and changes state."""

    def __init__(self) -> None:
        self._evidence_transition = EvidenceRecordingTransition(
            EvidenceAccumulator(),
        )
        self._evaluator = KnowledgeEvaluator()
        self._requirements = EvaluationRequirements(
            minimum_evidence=1,
        )
        self._promoter = KnowledgePromoter()

    def execute(
        self,
        artifact: KnowledgeArtifact,
    ) -> KnowledgeArtifact:
        if artifact.state is not KnowledgeState.OBSERVATION:
            return artifact

        artifact_with_evidence = self._evidence_transition.execute(
            artifact,
        )

        evaluation = self._evaluator.evaluate(
            artifact_with_evidence,
            source_state=KnowledgeState.OBSERVATION,
            requirements=self._requirements,
        )

        if not evaluation.eligible:
            return artifact_with_evidence

        return self._promoter.promote(
            artifact_with_evidence,
            KnowledgeState.HYPOTHESIS,
        )
