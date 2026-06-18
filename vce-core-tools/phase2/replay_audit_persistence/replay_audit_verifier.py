from phase2.replay_audit_persistence.replay_comparator_result import (
    ReplayComparatorResult,
)


class ReplayAuditVerifier:

    @staticmethod
    def verify(
        result: ReplayComparatorResult,
    ) -> bool:

        return (
            result.match
            and result.expected_hash
            == result.actual_hash
        )
