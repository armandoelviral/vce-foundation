from epics.epic088_replay_provenance_certificate.replay_provenance_certificate import (
    ReplayProvenanceCertificate,
)


class CertificateBuilder:

    @staticmethod
    def build(
        replay_id: str,
        request_hash: str,
        result_hash: str,
        environment_hash: str,
        comparator_hash: str,
    ) -> ReplayProvenanceCertificate:

        return ReplayProvenanceCertificate(
            replay_id=replay_id,
            request_hash=request_hash,
            result_hash=result_hash,
            environment_hash=environment_hash,
            comparator_hash=comparator_hash,
        )
