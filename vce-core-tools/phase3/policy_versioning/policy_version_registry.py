from phase3.policy_versioning.policy_version_record import (
    PolicyVersionRecord,
)


class PolicyVersionRegistry:

    def __init__(self):

        self._versions = {}

    def add(
        self,
        record: PolicyVersionRecord,
    ) -> None:

        key = (
            f"{record.policy_id}:"
            f"{record.version}"
        )

        self._versions[key] = record

    def get(
        self,
        version_id: str,
    ):

        return self._versions.get(
            version_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._versions
        )

    def version_ids(
        self,
    ):

        return list(
            self._versions.keys()
        )
