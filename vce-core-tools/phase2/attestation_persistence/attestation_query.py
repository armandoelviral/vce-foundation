class AttestationQuery:

    def __init__(self, store):

        self.store = store

    def by_subject(self, subject: str):

        return [
            record
            for record in self.store.all()
            if record.subject == subject
        ]
