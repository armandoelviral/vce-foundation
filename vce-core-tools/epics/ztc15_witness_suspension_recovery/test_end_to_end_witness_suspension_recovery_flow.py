from epics.ztc15_witness_suspension_recovery.witness_suspension_record import (
    WitnessSuspensionRecord,
)

from epics.ztc15_witness_suspension_recovery.suspension_registry import (
    SuspensionRegistry,
)

from epics.ztc15_witness_suspension_recovery.quorum_mutation_policy import (
    QuorumMutationPolicy,
)

from epics.ztc15_witness_suspension_recovery.recovery_record import (
    RecoveryRecord,
)

from epics.ztc15_witness_suspension_recovery.recovery_registry import (
    RecoveryRegistry,
)

from epics.ztc15_witness_suspension_recovery.witness_readmission_policy import (
    WitnessReadmissionPolicy,
)

from epics.ztc15_witness_suspension_recovery.witness_reinstatement_record import (
    WitnessReinstatementRecord,
)


def test_end_to_end_witness_suspension_recovery_flow():

    suspension_registry = SuspensionRegistry()

    suspension_registry.add(
        WitnessSuspensionRecord(
            witness_id="witness-003",
            reason="infrastructure_compromise",
        )
    )

    assert suspension_registry.is_suspended(
        "witness-003"
    )

    quorum_policy = QuorumMutationPolicy()

    assert quorum_policy.required_votes(
        total_witnesses=3,
        suspended_witnesses=1,
    ) == 2

    recovery_registry = RecoveryRegistry()

    recovery_registry.add(
        RecoveryRecord(
            witness_id="witness-003",
            recovery_reason="key_rotation_completed",
        )
    )

    readmission_policy = WitnessReadmissionPolicy()

    eligible = readmission_policy.is_eligible(
        suspended=suspension_registry.is_suspended("witness-003"),
        recovered=recovery_registry.is_recovered("witness-003"),
    )

    assert eligible is True

    reinstatement = WitnessReinstatementRecord(
        witness_id="witness-003",
        reinstatement_reason="readmission_approved",
    )

    assert reinstatement.witness_id == "witness-003"
    assert reinstatement.reinstatement_reason == "readmission_approved"
