import json


class SnapshotManager:

    def seal(
        self,
        state,
        path
    ):

        snapshot = {
            "sequence_number":
                state.sequence_number,

            "state_hash":
                state.state_hash,

            "event_count":
                len(state.events)
        }

        with open(
            path,
            "w"
        ) as file:

            json.dump(
                snapshot,
                file,
                indent=2
            )

        return snapshot
