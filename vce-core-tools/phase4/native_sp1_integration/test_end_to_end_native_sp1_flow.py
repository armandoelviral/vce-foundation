from phase4.native_sp1_integration.sp1_guest_program import (
    SP1GuestProgram,
)

from phase4.native_sp1_integration.sp1_proof_request import (
    SP1ProofRequest,
)

from phase4.native_sp1_integration.vcr_proof_adapter_bridge import (
    VCRProofAdapterBridge,
)

from phase4.native_sp1_integration.sp1_receipt_verification import (
    SP1ReceiptVerification,
)

from phase4.native_sp1_integration.d5_real_proof_attachment import (
    D5RealProofAttachment,
)

from phase4.native_sp1_integration.d7_real_browser_verification import (
    D7RealBrowserVerification,
)


def test_end_to_end_native_sp1_flow():

    program = SP1GuestProgram(
        program_id="sp1-guest-001",
        input_hash="input-hash-001",
        output_hash="output-hash-001",
    )

    request = SP1ProofRequest(
        request_id="proof-001",
        program_id=program.program_id,
        input_hash=program.input_hash,
    )

    bridge = VCRProofAdapterBridge()

    receipt = bridge.submit(
        request
    )

    assert (
        SP1ReceiptVerification.verify(
            receipt
        )
        is True
    )

    attachment = (
        D5RealProofAttachment.attach(
            d5_artifact_id="d5-001",
            receipt=receipt,
        )
    )

    assert (
        D7RealBrowserVerification.verify(
            attachment
        )
        is True
    )
