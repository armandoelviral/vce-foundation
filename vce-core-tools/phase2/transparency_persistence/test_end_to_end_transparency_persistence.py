from phase2.transparency_persistence.transparency_entry_record import (
    TransparencyEntryRecord,
)

from phase2.transparency_persistence.transparency_log_store import (
    TransparencyLogStore,
)

from phase2.transparency_persistence.transparency_query import (
    TransparencyQuery,
)

from phase2.transparency_persistence.merkle_root_record import (
    MerkleRootRecord,
)

from phase2.transparency_persistence.transparency_verifier import (
    TransparencyVerifier,
)

from phase2.transparency_persistence.transparency_report import (
    TransparencyReport,
)

from phase2.transparency_persistence.transparency_replay_binding import (
    TransparencyReplayBinding,
)


def test_end_to_end_transparency_flow():

    store = TransparencyLogStore()

    store.add(
        TransparencyEntryRecord(
            entry_id="entry-001",
            entry_hash="hash-001",
        )
    )

    query = TransparencyQuery(
        store
    )

    entries = query.by_hash(
        "hash-001"
    )

    assert len(entries) == 1

    root = MerkleRootRecord(
        root_hash="root-001",
        entry_count=len(entries),
    )

    verified = (
        TransparencyVerifier.verify(
            root,
            expected_root="root-001",
        )
    )

    assert verified is True

    report = TransparencyReport(
        [root]
    )

    assert (
        report.total_roots()
        == 1
    )

    binding = TransparencyReplayBinding(
        root_hash="root-001",
        replay_lsn=100,
    )

    assert binding.replay_lsn == 100
