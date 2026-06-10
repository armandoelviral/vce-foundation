from epics.epic079_cryptographic_agility_framework.hash_algorithm_registry import (
    HashAlgorithm,
    HashAlgorithmRegistry,
)


def build_registry():

    registry = HashAlgorithmRegistry()

    registry.register(
        HashAlgorithm(
            algorithm_id="sha-256",
            algorithm_name="SHA256",
            digest_length_bits=256,
            cryptographic_epoch="epoch-001",
            active=True,
        )
    )

    return registry


def test_registry_registers_hash_algorithm():

    registry = build_registry()

    algorithm = registry.get(
        "sha-256"
    )

    assert algorithm is not None


def test_registry_returns_hash_metadata():

    registry = build_registry()

    algorithm = registry.get(
        "sha-256"
    )

    assert algorithm.algorithm_name == "SHA256"
    assert algorithm.digest_length_bits == 256
    assert algorithm.cryptographic_epoch == "epoch-001"


def test_registry_lists_hash_algorithms():

    registry = build_registry()

    algorithms = registry.list_all()

    assert len(algorithms) == 1


def test_registry_supports_future_hash_algorithms():

    registry = build_registry()

    registry.register(
        HashAlgorithm(
            algorithm_id="sha3-512",
            algorithm_name="SHA3_512",
            digest_length_bits=512,
            cryptographic_epoch="epoch-002",
            active=False,
        )
    )

    algorithm = registry.get(
        "sha3-512"
    )

    assert algorithm.algorithm_name == "SHA3_512"
    assert algorithm.digest_length_bits == 512
