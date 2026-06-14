import json


class BrowserEvidenceParser:

    @staticmethod
    def parse(
        raw_json: str,
    ) -> dict:

        try:
            return json.loads(
                raw_json
            )
        except Exception as exc:
            raise ValueError(
                "invalid evidence json"
            ) from exc
