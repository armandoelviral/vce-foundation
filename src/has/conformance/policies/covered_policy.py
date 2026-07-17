from __future__ import annotations

from has.conformance.model.conformance_input import (
    ConformanceInput,
)
from has.conformance.model.decision import (
    Decision,
)
from has.conformance.model.evidence import (
    Evidence,
)
from has.conformance.policies.decision_policy import (
    DecisionPolicy,
)


class CoveredPolicy(DecisionPolicy):
    """
    Default policy implementing the
    initial Decision Model.
    """

    def evaluate(
        self,
        conformance_input: ConformanceInput,
        evidence: Evidence,
    ) -> Decision:

        if (
            conformance_input.is_covered()
            and evidence.available
        ):
            return Decision.CONFORMANT

        return Decision.NON_CONFORMANT
