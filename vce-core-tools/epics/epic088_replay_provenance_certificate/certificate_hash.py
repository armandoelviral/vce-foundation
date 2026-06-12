import hashlib
import json

from epics.epic088_replay_provenance_certificate.replay_provenance_certificate import (
    ReplayProvenanceCertificate,
)


class CertificateHash:

    @staticmethod
    def compute(
        certificate: ReplayProvenanceCertificate,
    ) -> str:

        payload = json.dumps(
            certificate.to_dict(),
            sort_keys=True,
        )

        return hashlib.sha256(
            payload.encode()
        ).hexdigest()
