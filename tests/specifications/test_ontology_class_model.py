from pathlib import Path

MODEL = Path(
    "research/commerce/ontology/"
    "ONTOLOGY_CLASS_MODEL.md"
)

CLASS_PROPERTIES = (
    "Reference one registered Knowledge Object.",
    "Possess one immutable Canonical Identifier.",
    "Declare one Preferred Name.",
    "Declare one Canonical Definition.",
    "Declare one Lifecycle Status.",
    "Declare one Domain Membership.",
)

RUNTIME_PROPERTIES = (
    "Deterministic.",
    "Auditable.",
    "Traceable.",
    "Canonical.",
    "Versioned.",
)


def model_text() -> str:
    return MODEL.read_text(encoding="utf-8")


def normalized_text() -> str:
    return " ".join(model_text().split())


def test_model_exists() -> None:
    assert MODEL.is_file()


def test_class_properties_exist() -> None:
    content = model_text()

    for item in CLASS_PROPERTIES:
        assert item in content


def test_identity_model_exists() -> None:
    content = normalized_text()

    assert (
        "Ontology Classes inherit the identity of "
        "their referenced Knowledge Object."
    ) in content

    assert (
        "No Ontology Class may redefine Canonical Identity."
    ) in content


def test_membership_model_exists() -> None:
    content = normalized_text()

    assert (
        "Every Knowledge Object belongs to exactly "
        "one primary Ontology Class."
    ) in content

    assert (
        "Secondary classifications shall be expressed "
        "through canonical relationships."
    ) in content


def test_constraints_exist() -> None:
    content = normalized_text()

    for rule in (
        "Ontology Classes shall not duplicate one another.",
        "Ontology Classes shall not redefine frozen canonical definitions.",
        "Ontology Classes shall remain traceable to the Knowledge Registry.",
    ):
        assert rule in content


def test_runtime_properties_exist() -> None:
    content = model_text()

    for item in RUNTIME_PROPERTIES:
        assert item in content


def test_release_criteria_exist() -> None:
    content = normalized_text()

    for criterion in (
        "Ontology Class definition exists.",
        "Identity model declared.",
        "Membership model declared.",
        "Constraints declared.",
        "Runtime properties declared.",
    ):
        assert criterion in content
