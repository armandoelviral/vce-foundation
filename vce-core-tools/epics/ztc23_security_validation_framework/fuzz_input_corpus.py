class FuzzInputCorpus:

    def __init__(self):

        self._inputs = []

    def add(
        self,
        payload,
    ):

        self._inputs.append(
            payload
        )

    def all(
        self,
    ):

        return list(
            self._inputs
        )

    def count(
        self,
    ):

        return len(
            self._inputs
        )
