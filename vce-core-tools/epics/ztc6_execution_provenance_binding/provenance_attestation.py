from epics.ztc6_execution_provenance_binding.artifact_hash_binding import (
    ArtifactHashBinding,
)

from epics.ztc6_execution_provenance_binding.execution_provenance_record import (
    ExecutionProvenanceRecord,
)


class ProvenanceAttestation:

    @staticmethod
    def build(
        record: ExecutionProvenanceRecord,
    ) -> dict:

        binding_hash = (
            ArtifactHashBinding.compute(
                artifact_hash=record.artifact_hash,
                execution_id=record.execution_id,
            )
        )

        return {
            "artifact_hash": record.artifact_hash,
            "execution_id": record.execution_id,
            "result_hash": record.result_hash,
            "binding_hash": binding_hash,
        }
