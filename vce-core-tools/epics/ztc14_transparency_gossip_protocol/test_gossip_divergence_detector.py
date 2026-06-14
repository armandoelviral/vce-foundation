from epics.ztc14_transparency_gossip_protocol.gossip_divergence_detector import (
    GossipDivergenceDetector,
)


def test_accepts_matching_roots():

    assert not GossipDivergenceDetector.detect(
        root_a="root-001",
        root_b="root-001",
    )


def test_detects_divergent_roots():

    assert GossipDivergenceDetector.detect(
        root_a="root-001",
        root_b="root-002",
    )


def test_detects_missing_root():

    assert GossipDivergenceDetector.detect(
        root_a="root-001",
        root_b="",
    )
