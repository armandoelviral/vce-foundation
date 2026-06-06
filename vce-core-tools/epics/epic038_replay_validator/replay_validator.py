class ReplayValidator:

    def validate(self, events):

        sequences = [
            event["sequence"]
            for event in events
        ]

        if sequences != sorted(sequences):
            return False

        if len(sequences) != len(set(sequences)):
            return False

        expected = list(
            range(
                sequences[0],
                sequences[-1] + 1,
            )
        )

        if sequences != expected:
            return False

        return True
