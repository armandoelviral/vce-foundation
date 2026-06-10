from epics.epic079_cryptographic_agility_framework.signature_algorithm_registry import (
    SignatureAlgorithm,
    SignatureAlgorithmRegistry,
)


def build_registry():

    registry = SignatureAlgorithmRegistry()

    registry.register(
        SignatureAlgorithm(
            algorithm_id="ecdsa-p256",
            algorithm_name="ECDSA_P256",
            cryptographic_epoch="epoch-001",
            active=True,
        )
    )

    return registry


def test_registry_registers_algorithm():

    registry = build_registry()

    algorithm = registry.get(
        "ecdsa-p256"
    )

    assert algorithm is not None


def test_registry_returns_algorithm_metadata():

    registry = build_registry()

    algorithm = registry.get(
        "ecdsa-p256"
    )

    assert (
        algorithm.algorithm_name
        == "ECDSA_P256"
    )

    assert (
        algorithm.cryptographic_epoch
        == "epoch-001"
    )


def test_registry_lists_algorithms():

    registry = build_registry()

    algorithms = registry.list_all()

    assert len(
        algorithms
    ) == 1


def test_registry_supports_future_pqc_algorithms():

    registry = build_registry()

    registry.register(
        SignatureAlgorithm(
            algorithm_id="ml-dsa-65",
            algorithm_name="ML_DSA_65",
            cryptographic_epoch="epoch-002",
            active=False,
        )
    )

    algorithm = registry.get(
        "ml-dsa-65"
    )

    assert (
        algorithm.algorithm_name
        == "ML_DSA_65"
    )
