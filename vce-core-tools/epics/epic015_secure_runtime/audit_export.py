import hashlib
import json
import time


class AuditTrailExport:

    def export(self, execution_result):

        record = {
            "timestamp": int(
                time.time()
            ),
            "execution": execution_result
        }

        canonical = json.dumps(
            record,
            sort_keys=True,
            separators=(",", ":")
        )

        digest = hashlib.sha256(
            canonical.encode()
        ).hexdigest()

        return {
            "audit_record": record,
            "audit_hash": digest
        }
