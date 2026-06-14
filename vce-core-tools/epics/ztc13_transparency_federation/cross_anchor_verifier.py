from epics.ztc13_transparency_federation.cross_anchor_record import (
    CrossAnchorRecord,
)


class CrossAnchorVerifier:

    def verify(
        self,
        record: CrossAnchorRecord,
    ) -> bool:

        return (
            record.source_anchor_id
            == record.target_anchor_id
        )
