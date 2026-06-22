from dataclasses import dataclass


@dataclass(frozen=True)
class ConstitutionalRight:

    right_id: str
    right_name: str

    def to_dict(self):

        return {
            "right_id":
                self.right_id,
            "right_name":
                self.right_name,
        }
