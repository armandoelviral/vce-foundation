class ReplayEnvironmentComparator:

    def compare(
        self,
        original_fingerprint,
        replay_fingerprint,
    ):

        if original_fingerprint.to_dict() == replay_fingerprint.to_dict():
            return {
                "result": "ENVIRONMENT_EQUIVALENT",
                "mismatches": [],
            }

        mismatches = []

        original = original_fingerprint.to_dict()
        replay = replay_fingerprint.to_dict()

        for key in original:

            if original[key] != replay.get(
                key
            ):
                mismatches.append(
                    key
                )

        return {
            "result": "ENVIRONMENT_MISMATCH",
            "mismatches": mismatches,
        }
