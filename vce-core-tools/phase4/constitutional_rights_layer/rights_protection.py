from dataclasses import dataclass


@dataclass(frozen=True)
class RightsProtection:

    right_id: str
    protected: bool

    def to_dict(self):

        return {
            "right_id": self.right_id,
            "protected": self.protected,
        }
