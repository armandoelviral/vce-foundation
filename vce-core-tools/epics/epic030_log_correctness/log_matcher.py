class LogMatcher:

    def compare(
        self,
        left_log,
        right_log
    ):

        limit = min(
            len(left_log),
            len(right_log)
        )

        for index in range(limit):

            left = left_log[index]
            right = right_log[index]

            if (
                left["sequence"]
                !=
                right["sequence"]
            ):

                return {
                    "match": False,
                    "conflict_index": index,
                    "left": left,
                    "right": right
                }

        return {
            "match": True,
            "conflict_index": None
        }
