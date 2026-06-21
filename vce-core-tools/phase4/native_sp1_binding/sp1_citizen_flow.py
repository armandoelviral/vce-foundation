from phase4.native_sp1_binding.sp1_citizen_record import (
    SP1CitizenRecord,
)

from phase4.native_sp1_binding.sp1_claim import (
    SP1Claim,
)

from phase4.native_sp1_binding.sp1_trust_verifier import (
    SP1TrustVerifier,
)


class SP1CitizenFlow:

    @staticmethod
    def generate():

        citizen_record = SP1CitizenRecord(
            tcu_did="did:tcn:test:01",
            program_id="fibonacci-program",
            verification_key="0x002a6f33375af18a2a8c01f54a5028b0164867416311f447a990dbb3c7b7",
            proof_digest="proof-digest-001",
            public_values={
                "n": 1,
                "a": 1,
                "b": 1,
            },
        )

        claim = SP1Claim(
            claim_id="claim-001",
            citizen_did=citizen_record.tcu_did,
            statement="fibonacci(1)=(1,1)",
            proof_digest=citizen_record.proof_digest,
        )

        trusted = SP1TrustVerifier.verify(
            claim
        )

        return {
            "citizen_record":
                citizen_record.to_dict(),
            "claim":
                claim.to_dict(),
            "trusted":
                trusted,
        }
