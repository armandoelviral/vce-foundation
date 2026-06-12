class PolicyVersioning:

    def __init__(
        self,
        policy_versions=None,
    ):

        self._policy_versions = (
            policy_versions
            if policy_versions is not None
            else {}
        )

    def add_version(
        self,
        policy_id,
        policy_version,
    ):

        if policy_id not in self._policy_versions:
            self._policy_versions[
                policy_id
            ] = []

        self._policy_versions[
            policy_id
        ].append(
            policy_version
        )

    def versions_for(
        self,
        policy_id,
    ):

        return list(
            self._policy_versions.get(
                policy_id,
                [],
            )
        )

    def latest_version(
        self,
        policy_id,
    ):

        versions = self.versions_for(
            policy_id
        )

        if not versions:
            return None

        return versions[-1]
