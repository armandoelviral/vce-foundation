from epics.epic092_deterministic_execution_policy.forbidden_capabilities import (
    ForbiddenCapabilities,
)


class DeterminismValidator:

    @staticmethod
    def validate(
        capabilities: set[str],
    ) -> bool:

        forbidden = (
            capabilities
            & ForbiddenCapabilities.ALL
        )

        return len(forbidden) == 0

