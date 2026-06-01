from epics.epic022_persistence.recovery_engine import (
    RecoveryEngine
)

from epics.epic022_persistence.crash_consistency import (
    CrashConsistencyChecker
)


class PersistenceVerification:

    def verify(
        self,
        db_path
    ):

        consistency = (
            CrashConsistencyChecker(
                db_path
            )
        ).verify()

        recovery = (
            RecoveryEngine(
                db_path
            )
        ).recover_checkpoint()

        return {
            "consistent":
                consistency[
                    "consistent"
                ],

            "recovered":
                recovery[
                    "recovered"
                ],

            "verified":
                (
                    consistency[
                        "consistent"
                    ]
                    and
                    recovery[
                        "recovered"
                    ]
                )
        }
