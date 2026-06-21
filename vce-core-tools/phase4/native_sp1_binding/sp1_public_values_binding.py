from dataclasses import dataclass


@dataclass(frozen=True)
class SP1PublicValuesBinding:

    tcu_did: str
    public_values: dict

    def to_dict(self):

        return {
            "tcu_did": self.tcu_did,
            "public_values":
                self.public_values,
        }
