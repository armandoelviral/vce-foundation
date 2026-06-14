from epics.ztc6_execution_provenance_binding.execution_provenance_record import (
    ExecutionProvenanceRecord,
)


class ProvenanceVerifier:

    @staticmethod
    def verify(
        record: ExecutionProvenanceRecord,
    ) -> bool:

        return all(
            [
                record.artifact_hash,
                record.execution_id,
                record.result_hash,
            ]
        )
