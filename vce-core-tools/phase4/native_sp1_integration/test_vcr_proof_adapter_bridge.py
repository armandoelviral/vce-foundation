from phase4.native_sp1_integration.sp1_proof_request import (
    SP1ProofRequest,
)

from phase4.native_sp1_integration.sp1_receipt_artifact import (
    SP1ReceiptArtifact,
)

from phase4.native_sp1_integration.vcr_proof_adapter_bridge import (
    VCRProofAdapterBridge,
)


def test_bridge_accepts_request():

    bridge = VCRProofAdapterBridge()

    request = SP1ProofRequest(
        request_id="proof-001",
        program_id="sp1-guest-001",
        input_hash="input-hash-001",
    )

    receipt = bridge.submit(
        request
    )

    assert (
        receipt.request_id
        == "proof-001"
    )


def test_bridge_returns_receipt():

    bridge = VCRProofAdapterBridge()

    request = SP1ProofRequest(
        request_id="proof-001",
        program_id="sp1-guest-001",
        input_hash="input-hash-001",
    )

    receipt = bridge.submit(
        request
    )

    assert isinstance(
        receipt,
        SP1ReceiptArtifact,
    )


def test_receipt_contains_proof_hash():

    bridge = VCRProofAdapterBridge()

    request = SP1ProofRequest(
        request_id="proof-001",
        program_id="sp1-guest-001",
        input_hash="input-hash-001",
    )

    receipt = bridge.submit(
        request
    )

    assert (
        receipt.proof_hash
        == "proof-proof-001"
    )


def test_receipt_contains_vk_hash():

    bridge = VCRProofAdapterBridge()

    request = SP1ProofRequest(
        request_id="proof-001",
        program_id="sp1-guest-001",
        input_hash="input-hash-001",
    )

    receipt = bridge.submit(
        request
    )

    assert (
        receipt.verification_key_hash
        == "vk-sp1-guest-001"
    )
