from dataclasses import dataclass


@dataclass(frozen=True)
class CatalogedProcess:
    process_id: str
    process_name: str
    active: bool


class ProcessCatalog:

    def __init__(self):

        self._processes = {}

    def register(
        self,
        process: CatalogedProcess,
    ):

        self._processes[
            process.process_id
        ] = process

    def get(
        self,
        process_id: str,
    ):

        return self._processes.get(
            process_id
        )

    def is_cataloged(
        self,
        process_id: str,
    ):

        process = self.get(
            process_id
        )

        return (
            process is not None
            and process.active is True
        )
