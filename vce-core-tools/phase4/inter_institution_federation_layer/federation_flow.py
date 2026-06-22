from phase4.inter_institution_federation_layer.institution_identity import (
    InstitutionIdentity,
)

from phase4.inter_institution_federation_layer.institution_registry import (
    InstitutionRegistry,
)

from phase4.inter_institution_federation_layer.delegated_authority import (
    DelegatedAuthority,
)

from phase4.inter_institution_federation_layer.inter_institution_trust import (
    InterInstitutionTrust,
)

from phase4.inter_institution_federation_layer.treaty_record import (
    TreatyRecord,
)

from phase4.inter_institution_federation_layer.cross_institution_dispute import (
    CrossInstitutionDispute,
)

from phase4.inter_institution_federation_layer.federation_state import (
    FederationState,
)


class FederationFlow:

    @staticmethod
    def generate():

        institution_a = InstitutionIdentity(
            institution_id="inst-001",
            institution_name="VCE Governance Council",
        )

        institution_b = InstitutionIdentity(
            institution_id="inst-002",
            institution_name="VCE Adjudication Council",
        )

        registry = InstitutionRegistry(
            institutions=[
                institution_a,
                institution_b,
            ]
        )

        delegation = DelegatedAuthority(
            source_institution="inst-001",
            target_institution="inst-002",
            authority="adjudication_review",
        )

        trust = InterInstitutionTrust(
            source_institution="inst-001",
            target_institution="inst-002",
            trusted=True,
        )

        treaty = TreatyRecord(
            treaty_id="treaty-001",
            institution_a="inst-001",
            institution_b="inst-002",
            treaty_type="mutual_adjudication",
        )

        dispute = CrossInstitutionDispute(
            dispute_id="dispute-001",
            institution_a="inst-001",
            institution_b="inst-002",
            treaty_id="treaty-001",
        )

        state = FederationState(
            federation_state="HEALTHY",
        )

        return {
            "registry":
                registry.to_dict(),
            "delegation":
                delegation.to_dict(),
            "trust":
                trust.to_dict(),
            "treaty":
                treaty.to_dict(),
            "dispute":
                dispute.to_dict(),
            "state":
                state.to_dict(),
        }
