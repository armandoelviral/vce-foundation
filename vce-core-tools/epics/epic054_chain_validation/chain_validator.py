class ChainValidator:

    def validate(self, records):

        known_hashes = {
            record.snapshot_hash
            for record in records
        }

        for record in records:
            if record.parent_hash is None:
                continue

            if record.parent_hash not in known_hashes:
                return False

        return True
