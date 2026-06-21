from phase4.trusted_compute_unit_registry.tcu_registry_flow import (
    TcuRegistryFlow,
)


def test_generates_registry_flow():

    result = TcuRegistryFlow.generate()

    assert "registry_hash" in result
    assert "entries" in result
    assert "member_verified" in result


def test_member_verified():

    result = TcuRegistryFlow.generate()

    assert result["member_verified"] is True


def test_registry_hash_present():

    result = TcuRegistryFlow.generate()

    assert len(result["registry_hash"]) == 64
