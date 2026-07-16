from has.runtime.evaluation_requirements import (
    EvaluationRequirements,
)
from has.runtime.evaluation_result import EvaluationResult
from has.runtime.knowledge_artifact import KnowledgeArtifact
from has.runtime.knowledge_state import KnowledgeState


class KnowledgeEvaluator:
    """Evaluates whether an artifact is ready to change state."""

    WRONG_SOURCE_STATE = "wrong_source_state"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    INSUFFICIENT_INDEPENDENT_VALIDATIONS = (
        "insufficient_independent_validations"
    )
    INSUFFICIENT_DESTRUCTION_ATTEMPTS = (
        "insufficient_destruction_attempts"
    )

    def evaluate(
        self,
        artifact: KnowledgeArtifact,
        *,
        source_state: KnowledgeState,
        requirements: EvaluationRequirements,
    ) -> EvaluationResult:
        reasons: list[str] = []

        if artifact.state is not source_state:
            reasons.append(self.WRONG_SOURCE_STATE)

        if artifact.evidence_count < requirements.minimum_evidence:
            reasons.append(self.INSUFFICIENT_EVIDENCE)

        if (
            artifact.independent_validations
            < requirements.minimum_independent_validations
        ):
            reasons.append(
                self.INSUFFICIENT_INDEPENDENT_VALIDATIONS
            )

        if (
            artifact.destruction_attempts
            < requirements.minimum_destruction_attempts
        ):
            reasons.append(
                self.INSUFFICIENT_DESTRUCTION_ATTEMPTS
            )

        if reasons:
            return EvaluationResult(
                eligible=False,
                reasons=tuple(reasons),
            )

        return EvaluationResult(eligible=True)
