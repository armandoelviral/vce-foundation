from has.runtime.knowledge_transition_policy import (
    KnowledgeTransitionPolicy,
)
from has.runtime.runtime_event import RuntimeEvent
from has.runtime.verification_result import VerificationResult


class RuntimeEventVerifier:
    """Verifies the semantic consistency of runtime events."""

    TRANSITION_NOT_ALLOWED = "transition_not_allowed"
    ARTIFACT_ID_REQUIRED = "artifact_id_required"
    EVENT_ID_REQUIRED = "event_id_required"
    ELIGIBLE_EVALUATION_REQUIRED = (
        "eligible_evaluation_required"
    )

    def __init__(
        self,
        policy: KnowledgeTransitionPolicy | None = None,
    ) -> None:
        self._policy = (
            policy
            if policy is not None
            else KnowledgeTransitionPolicy()
        )

    def verify(
        self,
        event: RuntimeEvent,
    ) -> VerificationResult:
        reasons: list[str] = []

        if not event.event_id.strip():
            reasons.append(
                self.EVENT_ID_REQUIRED,
            )

        if not event.artifact_id.strip():
            reasons.append(
                self.ARTIFACT_ID_REQUIRED,
            )

        if not event.evaluation.eligible:
            reasons.append(
                self.ELIGIBLE_EVALUATION_REQUIRED,
            )

        if not self._policy.is_allowed(
            event.from_state,
            event.to_state,
        ):
            reasons.append(
                self.TRANSITION_NOT_ALLOWED,
            )

        if reasons:
            return VerificationResult(
                valid=False,
                reasons=tuple(reasons),
            )

        return VerificationResult(
            valid=True,
        )
