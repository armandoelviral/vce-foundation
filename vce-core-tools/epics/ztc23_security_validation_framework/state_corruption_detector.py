class StateCorruptionDetector:

    def detect(
        self,
        expected: dict,
        observed: dict,
    ) -> dict:

        differences = []

        keys = (
            set(expected.keys())
            | set(observed.keys())
        )

        for key in keys:

            if (
                expected.get(key)
                != observed.get(key)
            ):
                differences.append(
                    key
                )

        return {
            "corrupted": len(
                differences
            ) > 0,
            "differences": differences,
        }
