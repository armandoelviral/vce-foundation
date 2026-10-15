from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ProtectedCaseAccessCredential:
    protection_key_id: str
    nonce: bytes = field(repr=False)
    ciphertext: bytes = field(repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.protection_key_id, str) or not self.protection_key_id.strip():
            raise ValueError("protection_key_id must be a nonempty string")
        if not isinstance(self.nonce, bytes) or len(self.nonce) != 12:
            raise ValueError("nonce must contain exactly 12 bytes")
        if not isinstance(self.ciphertext, bytes) or len(self.ciphertext) <= 16:
            raise ValueError("ciphertext must contain encrypted credential and tag")
