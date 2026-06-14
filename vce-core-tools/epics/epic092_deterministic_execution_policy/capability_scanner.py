from typing import Iterable
from typing import Set


class CapabilityScanner:

    @staticmethod
    def scan(
        imports: Iterable[str],
    ) -> Set[str]:

        return set(imports)
