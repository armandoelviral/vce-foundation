from epics.epic080_governance_drift_detection.governance_whitelist import (
    GovernanceWhitelist,
)


class TransactionBlockingRule:

    def __init__(
        self,
        whitelist: GovernanceWhitelist,
    ):

        self._whitelist = whitelist

    def should_block(
        self,
        fingerprint,
    ):

        return not self._whitelist.is_approved(
            fingerprint
        )

    def decision(
        self,
        fingerprint,
    ):

        if self.should_block(
            fingerprint
        ):
            return {
                "allowed": False,
                "reason": "GOVERNANCE_DRIFT_DETECTED",
            }

        return {
            "allowed": True,
            "reason": "APPROVED_GOVERNANCE_BASELINE",
        }
