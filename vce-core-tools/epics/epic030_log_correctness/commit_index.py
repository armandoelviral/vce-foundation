class CommitIndex:

    def __init__(self):

        self.value = 0

    def advance(
        self,
        sequence
    ):

        if sequence > self.value:

            self.value = sequence

        return self.value
