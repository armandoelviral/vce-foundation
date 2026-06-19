from phase3.certificate_transparency.transparency_log import (
    TransparencyLog,
)


class TransparencyReport:

    def __init__(
        self,
        log: TransparencyLog,
    ):

        self.log = log

    def entry_count(
        self,
    ) -> int:

        return self.log.count()

    def entry_ids(
        self,
    ):

        return [
            entry.entry_id
            for entry in self.log.entries()
        ]

    def to_dict(
        self,
    ):

        return {
            "entry_count":
                self.entry_count(),
            "entry_ids":
                self.entry_ids(),
        }
