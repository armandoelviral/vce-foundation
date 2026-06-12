class VersionPinnedPolicyResolution:

    def __init__(
        self,
        policy_registry,
    ):

        self._policy_registry = policy_registry

    def resolve(
        self,
        policy_id,
        policy_version,
    ):

        return self._policy_registry.get(
            policy_id,
            policy_version,
        )
