def verify_anchor_receipt(
    ledger_root,
    receipt,
):

    return (
        receipt.status == "ANCHORED"
        and receipt.root_hash == ledger_root.root_hash
    )
