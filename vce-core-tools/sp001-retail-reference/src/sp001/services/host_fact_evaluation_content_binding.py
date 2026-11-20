"""Content correspondence verification without authority."""

import hmac

from sp001.contracts.host_fact_assertion import HostFactAssertion
from sp001.contracts.host_fact_evaluation import HostFactEvaluation
from sp001.contracts.host_fact_evaluation_content_binding import (
    HostFactEvaluationContentBinding,
)
from sp001.services.host_fact_assertion_digest import (
    digest_host_fact_assertion,
)


def verify_host_fact_evaluation_content_binding(
    binding: HostFactEvaluationContentBinding,
    assertion: HostFactAssertion,
    evaluation: HostFactEvaluation,
) -> bool:
    """Verify content correspondence, not authenticity or findings."""

    if type(binding) is not HostFactEvaluationContentBinding:
        raise TypeError("invalid binding type")

    if type(assertion) is not HostFactAssertion:
        raise TypeError("invalid assertion type")

    if type(evaluation) is not HostFactEvaluation:
        raise TypeError("invalid evaluation type")

    if binding.evaluation_record_id != evaluation.evaluation_record_id:
        return False

    if binding.assertion_id != assertion.assertion_id:
        return False

    if evaluation.assertion_id != assertion.assertion_id:
        return False

    if evaluation.evaluation_id != assertion.evaluation_id:
        return False

    if evaluation.policy_version != assertion.policy_version:
        return False

    calculated_digest = digest_host_fact_assertion(assertion)

    return hmac.compare_digest(
        binding.assertion_digest,
        calculated_digest,
    )
