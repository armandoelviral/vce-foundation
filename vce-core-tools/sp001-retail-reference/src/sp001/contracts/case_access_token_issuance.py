from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class IssuedCaseAccessToken:
    """Credential value; construction does not establish trusted issuance."""

    credential: str = field(repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.credential, str):
            raise TypeError("credential must be a string")
        if not self.credential:
            raise ValueError("credential must not be empty")
        if any(character.isspace() or ord(character) < 32
               or ord(character) == 127 for character in self.credential):
            raise ValueError("credential must not contain whitespace or controls")
