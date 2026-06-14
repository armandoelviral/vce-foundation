from epics.ztc10_multi_party_verification.witness_provider_metadata import (
    WitnessProviderMetadata,
)


def test_provider_metadata_contains_cloud_identity():

    metadata = WitnessProviderMetadata(
        witness_id="witness-001",
        cloud_provider="aws",
        region="us-east-1",
        kms_provider="aws-kms",
        confidential_compute_profile="nitro",
    )

    assert metadata.witness_id == "witness-001"
    assert metadata.cloud_provider == "aws"
    assert metadata.region == "us-east-1"
    assert metadata.kms_provider == "aws-kms"
    assert metadata.confidential_compute_profile == "nitro"


def test_provider_metadata_serializes():

    metadata = WitnessProviderMetadata(
        witness_id="witness-001",
        cloud_provider="aws",
        region="us-east-1",
        kms_provider="aws-kms",
        confidential_compute_profile="nitro",
    )

    assert metadata.to_dict() == {
        "witness_id": "witness-001",
        "cloud_provider": "aws",
        "region": "us-east-1",
        "kms_provider": "aws-kms",
        "confidential_compute_profile": "nitro",
    }
