class WALRecovery:

    def detect_truncation(
        self,
        wal_lines,
    ):

        for line in wal_lines:

            parts = line.split("|")

            if len(parts) != 3:
                return True

        return False

    def detect_corruption(
        self,
        record,
    ):

        parts = record.split("|")

        if len(parts) != 3:
            return True

        lsn, opcode, payload = parts

        if not lsn.isdigit():
            return True

        if opcode == "":
            return True

        if payload == "":
            return True

        return False

    def recover_until_corruption(
        self,
        wal_lines,
    ):

        recovered = []

        for line in wal_lines:

            if self.detect_corruption(line):
                break

            recovered.append(line)

        return recovered

    def recover_after_crash(
        self,
        wal_lines,
    ):

        return self.recover_until_corruption(
            wal_lines
        )
