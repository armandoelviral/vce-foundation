import json

from epics.epic051_signed_snapshot_attestation.signed_attestation import (
    SignedSnapshotAttestation,
)


class AttestationSigner:

    def __init__(self, signer):
        self.signer = signer

    def _payload(self, sequence, state_hash):
        return json.dumps(
            {
                "sequence": sequence,
                "state_hash": state_hash,
            },
            sort_keys=True,
            separators=(",", ":"),
        )

    def sign(self, attestation):
        payload = self._payload(
            attestation.sequence,
            attestation.state_hash,
        )

        signature = self.signer.sign(payload)

        return SignedSnapshotAttestation(
            sequence=attestation.sequence,
            state_hash=attestation.state_hash,
            signature=signature,
        )

    def verify(self, signed_attestation):
        payload = self._payload(
            signed_attestation.sequence,
            signed_attestation.state_hash,
        )

        return self.signer.verify(
            payload,
            signed_attestation.signature,
        )
