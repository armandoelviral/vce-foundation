from __future__ import annotations

from has.conformance.decision_evaluator import (
    ConformanceDecisionEvaluator,
)
from has.conformance.model.conformance_input import (
    ConformanceInput,
)
from has.conformance.model.decision_record import (
    DecisionRecord,
)
from has.conformance.model.evidence import (
    Evidence,
)


class ConformancePipeline:
    """
    Application facade for conformance evaluation.

    The pipeline coordinates domain objects and delegates
    all decision semantics to ConformanceDecisionEvaluator.
    """

    def __init__(
        self,
        evaluator: ConformanceDecisionEvaluator | None = None,
    ) -> None:
        self._evaluator = (
            evaluator
            if evaluator is not None
            else ConformanceDecisionEvaluator()
        )

    def evaluate(
        self,
        conformance_input: ConformanceInput,
        evidence: Evidence,
    ) -> DecisionRecord:
        return self._evaluator.evaluate(
            conformance_input,
            evidence,
        )
