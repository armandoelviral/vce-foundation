from epics.epic072_executable_veracity_artifact.ledger_anchor import (
    AnchorReceipt,
)

from epics.epic072_executable_veracity_artifact.veracity_artifact import (
    VeracityArtifact,
)


def verify_artifact(
    artifact: VeracityArtifact,
    receipt: AnchorReceipt,
):

    return (
        artifact.compute_hash()
        ==
        receipt.artifact_hash
    )
