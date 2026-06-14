from dataclasses import dataclass
import secrets


@dataclass(frozen=True)
class SigningKeyPair:
    private_key: str
    public_key: str

    @classmethod
    def generate(cls):

        return cls(
            private_key=secrets.token_hex(32),
            public_key=secrets.token_hex(32),
        )
