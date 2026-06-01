from epics.epic014_runtime_hardening.schema_firewall import SchemaFirewall
from epics.epic014_runtime_hardening.opcode_policy import OpcodePolicy
from epics.epic014_runtime_hardening.replay_attack_detector import ReplayAttackDetector
from epics.epic014_runtime_hardening.resource_limits import ResourceLimits

from epics.epic013_external_trust.provenance_engine import ProvenanceEngine


class SecureExecutionEngine:

    def __init__(self):

        self.schema = SchemaFirewall()
        self.policy = OpcodePolicy()
        self.replay = ReplayAttackDetector()
        self.limits = ResourceLimits()

        self.provenance = ProvenanceEngine()


    def execute(
        self,
        events,
        certificate
    ):

        guards = (
            self.schema.validate_stream(
                events
            )
            and
            self.policy.validate_stream(
                events
            )
            and
            self.replay.validate_stream(
                events
            )
            and
            self.limits.validate_stream(
                events
            )
        )

        if not guards:

            return {
                "status": "REJECTED",
                "stage": "HARDENING"
            }

        result = (
            self.provenance.execute(
                events,
                certificate
            )
        )

        return {
            "status": "ACCEPTED",
            "result": result
        }
