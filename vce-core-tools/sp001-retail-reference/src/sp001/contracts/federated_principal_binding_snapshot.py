from dataclasses import dataclass

from sp001.contracts.case_access_issuance_preparation import FederatedPrincipalBinding


@dataclass(frozen=True, slots=True)
class FederatedPrincipalBindingSnapshot:
    binding: FederatedPrincipalBinding
    active: bool

    def __post_init__(self) -> None:
        if not isinstance(self.binding, FederatedPrincipalBinding):
            raise TypeError("binding must be a FederatedPrincipalBinding")
        if type(self.active) is not bool:
            raise TypeError("active must be an exact bool")
