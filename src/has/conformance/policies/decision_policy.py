from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from has.conformance.model.conformance_input import (
    ConformanceInput,
)
from has.conformance.model.decision import (
    Decision,
)
from has.conformance.model.evidence import (
    Evidence,
)


class DecisionPolicy(ABC):
    """
    Strategy used by the Conformance
    Evaluator to derive a Decision.
    """

    @abstractmethod
    def evaluate(
        self,
        conformance_input: ConformanceInput,
        evidence: Evidence,
    ) -> Decision:
        """
        Return the normative Decision.
        """
        raise NotImplementedError
