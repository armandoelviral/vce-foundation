from dataclasses import dataclass


@dataclass(frozen=True)
class TcuDid:

    value: str

    def __post_init__(self):

        if not self.value:

            raise ValueError(
                "did cannot be empty"
            )

    def to_dict(self):

        return {
            "did": self.value,
        }
