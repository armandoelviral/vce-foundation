from phase3.trust_policy_engine.trust_policy_record import (
    TrustPolicyRecord,
)


class TrustEvaluation:

    @staticmethod
    def evaluate(
        policy: TrustPolicyRecord,
        certificate_exists: bool,
        certificate_published: bool,
        certificate_revoked: bool,
    ) -> bool:

        if not certificate_exists:
            return False

        if not certificate_published:
            return False

        if certificate_revoked:
            return False

        return True
