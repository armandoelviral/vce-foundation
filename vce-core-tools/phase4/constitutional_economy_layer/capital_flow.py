from phase4.constitutional_economy_layer.capital_record import (
    CapitalRecord,
)

from phase4.constitutional_economy_layer.capital_registry import (
    CapitalRegistry,
)

from phase4.constitutional_economy_layer.capital_accrual import (
    CapitalAccrual,
)

from phase4.constitutional_economy_layer.capital_loss import (
    CapitalLoss,
)

from phase4.constitutional_economy_layer.capital_delegation import (
    CapitalDelegation,
)

from phase4.constitutional_economy_layer.capital_state import (
    CapitalState,
)

from phase4.constitutional_economy_layer.capital_verifier import (
    CapitalVerifier,
)


class CapitalFlow:

    @staticmethod
    def generate():

        record = CapitalRecord(
            identity_id="identity-001",
            capital=100,
        )

        registry = CapitalRegistry(
            records=[record]
        )

        accrual = CapitalAccrual(
            identity_id="identity-001",
            amount=25,
        )

        loss = CapitalLoss(
            identity_id="identity-001",
            amount=10,
        )

        delegation = CapitalDelegation(
            delegator_id="identity-001",
            delegate_id="identity-002",
            amount=25,
        )

        state = CapitalState(
            balance=90,
        )

        valid = CapitalVerifier.verify(
            state
        )

        return {
            "record":
                record.to_dict(),
            "registry":
                registry.to_dict(),
            "accrual":
                accrual.to_dict(),
            "loss":
                loss.to_dict(),
            "delegation":
                delegation.to_dict(),
            "state":
                state.to_dict(),
            "valid":
                valid,
        }
