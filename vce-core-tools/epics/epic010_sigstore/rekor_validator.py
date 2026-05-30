#!/usr/bin/env python3

class RekorValidator:

    def verify_inclusion_proof(
        self,
        rekor_entry_response: dict
    ) -> bool:

        if not rekor_entry_response:
            return False

        for _, entry in rekor_entry_response.items():

            verification = entry.get(
                "verification",
                {}
            )

            signed_entry_timestamp = verification.get(
                "signedEntryTimestamp",
                ""
            )

            if not signed_entry_timestamp:
                return False

        return True
