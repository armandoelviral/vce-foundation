from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeConfigurationSnapshot:
    runtime_version: str
    policy_version: str
    execution_profile: str
    configuration_hash: str

    def to_dict(self):

        return {
            "runtime_version": self.runtime_version,
            "policy_version": self.policy_version,
            "execution_profile": self.execution_profile,
            "configuration_hash": self.configuration_hash,
        }
