from dataclasses import dataclass


@dataclass(frozen=True)
class TransparencyAnchor:

    attestation_id: str
    anchor_id: str
    transparency_root: str
