from collections import defaultdict

from epics.phase4_026_institutional_capital.institutional_capital_record import (
    InstitutionalCapitalRecord,
)


class InstitutionalCapitalRegistry:
    def __init__(self):
        self._records_by_institution: dict[str, list[InstitutionalCapitalRecord]] = (
            defaultdict(list)
        )
        self._evidence_index: set[tuple[str, str]] = set()

    def add(self, record: InstitutionalCapitalRecord) -> None:
        evidence_key = (record.institution_id, record.evidence_id)

        if evidence_key in self._evidence_index:
            raise ValueError("duplicate evidence for institution")

        self._records_by_institution[record.institution_id].append(record)
        self._evidence_index.add(evidence_key)

    def records_for(self, institution_id: str) -> list[InstitutionalCapitalRecord]:
        return list(self._records_by_institution.get(institution_id, []))
