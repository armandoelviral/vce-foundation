from epics.phase6_005_constitutional_trust_score.trust_score_record import (
    TrustScoreRecord,
)


class TrustScoreRegistry:
    def __init__(self):
        self._records = []

    def add(self, record: TrustScoreRecord):
        self._records.append(record)

    def records(self):
        return list(self._records)
