from epics.phase4_026_institutional_capital.institutional_capital_state import (
    InstitutionalCapitalState,
)
from epics.phase4_026_institutional_capital.institutional_capital_registry import (
    InstitutionalCapitalRegistry,
)


def verify_institutional_capital(
    registry: InstitutionalCapitalRegistry,
    institution_id: str,
    required_capital: int,
) -> dict:
    if required_capital < 0:
        raise ValueError("required_capital cannot be negative")

    state = InstitutionalCapitalState.from_registry(
        registry=registry,
        institution_id=institution_id,
    )

    return {
        "institution_id": institution_id,
        "verified": state.total_capital >= required_capital,
        "total_capital": state.total_capital,
        "required_capital": required_capital,
        "record_count": state.record_count,
    }
