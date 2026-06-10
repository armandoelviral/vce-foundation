def verify_weight_hash(
    manifest,
    fingerprint,
):

    return (
        manifest.weights_hash
        ==
        fingerprint.weights_hash
    )
