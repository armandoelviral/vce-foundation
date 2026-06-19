from phase3.certificate_transparency.transparency_log import (
    TransparencyLog,
)


class TransparencyQuery:

    def __init__(
        self,
        log: TransparencyLog,
    ):

        self.log = log

    def by_id(
        self,
        entry_id: str,
    ):

        return self.log.get(
            entry_id
        )
