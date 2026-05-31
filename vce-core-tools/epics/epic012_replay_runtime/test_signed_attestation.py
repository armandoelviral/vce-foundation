from signed_attestation import SignedAttestation


attestation = {
    "runtime": "VCE-RTE",
    "state_hash": "abc123",
    "verified": True
}


signer = SignedAttestation()

signed = signer.sign(
    attestation
)

print(
    signer.verify(
        signed
    )
)
