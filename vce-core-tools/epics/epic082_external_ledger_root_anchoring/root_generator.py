import hashlib
import json

from epics.epic082_external_ledger_root_anchoring.ledger_root import (
    LedgerRoot,
)


def generate_ledger_root(
    evidence_records,
    region,
    generated_at,
):

    canonical_records = json.dumps(
        evidence_records,
        sort_keys=True,
        separators=(",", ":"),
    )

    root_hash = hashlib.sha256(
        canonical_records.encode("utf-8")
    ).hexdigest()

    sequences = [
        record["sequence"]
        for record in evidence_records
    ]

    return LedgerRoot(
        root_hash=root_hash,
        sequence_start=min(sequences),
        sequence_end=max(sequences),
        evidence_count=len(evidence_records),
        region=region,
        generated_at=generated_at,
    )
