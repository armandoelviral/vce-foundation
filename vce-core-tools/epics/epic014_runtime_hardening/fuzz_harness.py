import random
import string

from epics.epic014_runtime_hardening.schema_firewall import SchemaFirewall
from epics.epic014_runtime_hardening.opcode_policy import OpcodePolicy
from epics.epic014_runtime_hardening.resource_limits import ResourceLimits


class FuzzHarness:

    def __init__(self):

        self.schema = SchemaFirewall()
        self.policy = OpcodePolicy()
        self.limits = ResourceLimits()


    def random_event(self):

        return {
            "lsn": random.choice(
                [
                    1,
                    "bad",
                    None
                ]
            ),

            "opcode": random.choice(
                [
                    "APPEND_EVIDENCE",
                    "DELETE_SYSTEM",
                    "",
                ]
            ),

            "payload": "".join(
                random.choices(
                    string.ascii_letters,
                    k=random.randint(
                        1,
                        2000
                    )
                )
            )
        }


    def run(self, iterations=100):

        rejected = 0
        accepted = 0

        for _ in range(iterations):

            events = [
                self.random_event()
            ]


            result = (
                self.schema.validate_stream(events)
                and self.policy.validate_stream(events)
                and self.limits.validate_stream(events)
            )


            if result:
                accepted += 1
            else:
                rejected += 1


        return {
            "accepted": accepted,
            "rejected": rejected,
            "completed": True
        }
