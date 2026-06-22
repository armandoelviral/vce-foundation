from phase4.admission_policy_layer.admission_requirement import (
    AdmissionRequirement,
)

from phase4.admission_policy_layer.admission_policy import (
    AdmissionPolicy,
)

from phase4.admission_policy_layer.admission_state import (
    AdmissionState,
)

from phase4.admission_policy_layer.admission_verifier import (
    AdmissionVerifier,
)


class AdmissionFlow:

    @staticmethod
    def generate():

        requirement = AdmissionRequirement(
            requirement_name="minimum_reputation",
            requirement_value=100,
        )

        policy = AdmissionPolicy(
            policy_name="citizen_admission_policy",
            requirements=[
                "minimum_reputation",
                "response_validity",
            ],
        )

        state = AdmissionState(
            citizen_did="did:tcn:test:01",
            admission_state="ADMITTED",
        )

        participation_allowed = (
            AdmissionVerifier.verify(
                state
            )
        )

        return {
            "requirement":
                requirement.to_dict(),
            "policy":
                policy.to_dict(),
            "state":
                state.to_dict(),
            "participation_allowed":
                participation_allowed,
        }
