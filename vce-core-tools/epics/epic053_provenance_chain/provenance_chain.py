class ProvenanceChain:

    def __init__(self):
        self._records = {}

    def add(self, record):
        self._records[
            record.snapshot_hash
        ] = record

    def latest(self):

        if not self._records:
            return None

        return list(
            self._records.values()
        )[-1]

    def parent_of(
        self,
        snapshot_hash,
    ):

        record = self._records[
            snapshot_hash
        ]

        parent_hash = (
            record.parent_hash
        )

        if parent_hash is None:
            return None

        return self._records[
            parent_hash
        ]
