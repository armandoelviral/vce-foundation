from epics.epic092_deterministic_execution_policy.determinism_validator import (
    DeterminismValidator,
)

from epics.epic092_deterministic_execution_policy.host_import_policy import (
    HostImportPolicy,
)


class ModuleAdmissionGate:

    @staticmethod
    def admit(
        capabilities: set[str],
    ) -> bool:

        if not DeterminismValidator.validate(
            capabilities
        ):
            return False

        return all(
            HostImportPolicy.is_allowed(
                capability
            )
            for capability in capabilities
        )
