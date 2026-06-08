from dataclasses import dataclass

from epics.epic072_executable_veracity_artifact.veracity_artifact import (
    VeracityArtifact,
)


@dataclass(frozen=True)
class AnchorReceipt:
    artifact_hash: str
    ledger_sequence: int
    ledger_state_hash: str
    anchoring_status: str


def anchor_artifact(
    artifact: VeracityArtifact,
    ledger_sequence: int = 1,
):

    artifact_hash = artifact.compute_hash()

    ledger_state_hash = artifact_hash

    return AnchorReceipt(
        artifact_hash=artifact_hash,
        ledger_sequence=ledger_sequence,
        ledger_state_hash=ledger_state_hash,
        anchoring_status="ANCHORED",
    )
