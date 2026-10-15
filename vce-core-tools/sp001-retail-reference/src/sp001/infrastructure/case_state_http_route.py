from urllib.parse import quote

CASE_STATE_ROUTE = "/v1/cases/{caseId}/state"


def validate_case_path_id(case_id: str) -> None:
    if not isinstance(case_id, str):
        raise TypeError("case_id must be a string")
    if (
        not case_id.strip()
        or case_id in {".", ".."}
        or "/" in case_id
        or "\\" in case_id
        or any(ord(character) < 32 or ord(character) == 127
               for character in case_id)
    ):
        raise ValueError("case_id must identify one valid URL path segment")


def case_state_path(case_id: str) -> str:
    validate_case_path_id(case_id)
    return CASE_STATE_ROUTE.replace("{caseId}", quote(case_id, safe=""))
