from epics.epic072_executable_veracity_artifact.artifact_verifier import (
    verify_artifact,
)
from epics.epic072_executable_veracity_artifact.ledger_anchor import (
    anchor_artifact,
)
from epics.epic072_executable_veracity_artifact.veracity_artifact import (
    VeracityArtifact,
)


class VeracityRuntime:

    def create_artifact(
        self,
        identity,
        trust,
        provenance,
        replay,
        evidence,
        governance,
    ):

        return VeracityArtifact(
            identity=identity,
            trust=trust,
            provenance=provenance,
            replay=replay,
            evidence=evidence,
            governance=governance,
        )

    def anchor(
        self,
        artifact,
        ledger_sequence=1,
    ):

        return anchor_artifact(
            artifact,
            ledger_sequence=ledger_sequence,
        )

    def verify(
        self,
        artifact,
        receipt,
    ):

        return verify_artifact(
            artifact,
            receipt,
        )
