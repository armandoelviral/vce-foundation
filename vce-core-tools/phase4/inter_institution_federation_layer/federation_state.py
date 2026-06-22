from dataclasses import dataclass


@dataclass(frozen=True)
class FederationState:

    federation_state: str

    def to_dict(self):

        return {
            "federation_state":
                self.federation_state,
        }
