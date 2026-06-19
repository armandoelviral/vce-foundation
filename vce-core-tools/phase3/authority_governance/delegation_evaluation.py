from phase3.authority_governance.authority_record import (
    AuthorityRecord,
)


class DelegationEvaluation:

    @staticmethod
    def evaluate(
        authority: AuthorityRecord,
    ) -> bool:

        return (
            authority.role
            == "GOVERNOR"
        )
