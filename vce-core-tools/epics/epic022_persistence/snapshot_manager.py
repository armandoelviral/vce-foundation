import json


class SnapshotManager:

    def save(
        self,
        snapshot_path,
        state
    ):

        with open(
            snapshot_path,
            "w"
        ) as handle:

            json.dump(
                state,
                handle,
                indent=2
            )

        return True


    def load(
        self,
        snapshot_path
    ):

        with open(
            snapshot_path,
            "r"
        ) as handle:

            return json.load(
                handle
            )

