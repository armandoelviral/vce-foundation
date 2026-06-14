from epics.ztc14_transparency_gossip_protocol.gossip_consistency_report import (
    GossipConsistencyReport,
)


def test_report_contains_registry_ids():

    report = GossipConsistencyReport(
        registry_a="registry-a",
        registry_b="registry-b",
        consistent=True,
    )

    assert report.registry_a == "registry-a"
    assert report.registry_b == "registry-b"


def test_report_contains_consistency_status():

    report = GossipConsistencyReport(
        registry_a="registry-a",
        registry_b="registry-b",
        consistent=True,
    )

    assert report.consistent is True


def test_report_serializes():

    report = GossipConsistencyReport(
        registry_a="registry-a",
        registry_b="registry-b",
        consistent=False,
    )

    assert report.to_dict() == {
        "registry_a": "registry-a",
        "registry_b": "registry-b",
        "consistent": False,
    }
