from phase3.historical_replay_auditor.historical_replay_record import (
    HistoricalReplayRecord,
)

from phase3.historical_replay_auditor.replay_evidence_resolver import (
    ReplayEvidenceResolver,
)

from phase3.replay_evidence_bundle.replay_evidence_record import (
    ReplayEvidenceRecord,
)

from phase3.replay_evidence_bundle.replay_evidence_bundle import (
    ReplayEvidenceBundle,
)


def test_resolver_returns_bundle():

    bundle = ReplayEvidenceBundle()

    bundle.add(
        ReplayEvidenceRecord(
            evidence_id="policy-001",
            evidence_type="policy",
        )
    )

    bundles = {
        "bundle-001": bundle
    }

    replay = HistoricalReplayRecord(
        replay_id="replay-001",
        bundle_id="bundle-001",
    )

    resolved = (
        ReplayEvidenceResolver.resolve(
            replay,
            bundles,
        )
    )

    assert resolved == bundle


def test_missing_bundle_returns_none():

    replay = HistoricalReplayRecord(
        replay_id="replay-001",
        bundle_id="missing",
    )

    resolved = (
        ReplayEvidenceResolver.resolve(
            replay,
            {},
        )
    )

    assert resolved is None


def test_resolved_bundle_contains_evidence():

    bundle = ReplayEvidenceBundle()

    bundle.add(
        ReplayEvidenceRecord(
            evidence_id="policy-001",
            evidence_type="policy",
        )
    )

    replay = HistoricalReplayRecord(
        replay_id="replay-001",
        bundle_id="bundle-001",
    )

    resolved = (
        ReplayEvidenceResolver.resolve(
            replay,
            {"bundle-001": bundle},
        )
    )

    assert resolved.count() == 1
