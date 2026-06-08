import json

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

    def prove(
        self,
        identity,
        trust,
        provenance,
        replay,
        evidence,
        governance,
        ledger_sequence=1,
    ):

        artifact = self.create_artifact(
            identity=identity,
            trust=trust,
            provenance=provenance,
            replay=replay,
            evidence=evidence,
            governance=governance,
        )

        receipt = self.anchor(
            artifact,
            ledger_sequence=ledger_sequence,
        )

        verified = self.verify(
            artifact,
            receipt,
        )

        return {
            "artifact": artifact,
            "receipt": receipt,
            "verified": verified,
        }
       
    def export_proof(
        self,
        proof,
    ):

        receipt = proof["receipt"]

        payload = {
            "artifact_hash": receipt.artifact_hash,
            "ledger_sequence": receipt.ledger_sequence,
            "verified": proof["verified"],
        }

        return json.dumps(
            payload,
            sort_keys=True,
        )

    def audit_proof(
        self,
        proof,
    ):

        verified = self.verify(
            proof["artifact"],
            proof["receipt"],
        )

        return {
            "audit_status": "PASSED" if verified else "FAILED",
            "verified": verified,
            "artifact_hash": proof["receipt"].artifact_hash,
            "ledger_sequence": proof["receipt"].ledger_sequence,
        }
