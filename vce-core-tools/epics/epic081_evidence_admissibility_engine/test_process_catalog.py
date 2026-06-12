from epics.epic081_evidence_admissibility_engine.process_catalog import (
    CatalogedProcess,
    ProcessCatalog,
)


def build_catalog():

    catalog = ProcessCatalog()

    catalog.register(
        CatalogedProcess(
            process_id="credit-risk-v7",
            process_name="Credit Risk Model",
            active=True,
        )
    )

    return catalog


def test_catalog_registers_process():

    catalog = build_catalog()

    process = catalog.get(
        "credit-risk-v7"
    )

    assert process is not None


def test_catalog_returns_process_metadata():

    catalog = build_catalog()

    process = catalog.get(
        "credit-risk-v7"
    )

    assert (
        process.process_name
        == "Credit Risk Model"
    )


def test_catalog_accepts_registered_process():

    catalog = build_catalog()

    assert (
        catalog.is_cataloged(
            "credit-risk-v7"
        )
        is True
    )


def test_catalog_rejects_unknown_process():

    catalog = build_catalog()

    assert (
        catalog.is_cataloged(
            "unknown-process"
        )
        is False
    )


def test_catalog_rejects_inactive_process():

    catalog = ProcessCatalog()

    catalog.register(
        CatalogedProcess(
            process_id="legacy-model",
            process_name="Legacy Model",
            active=False,
        )
    )

    assert (
        catalog.is_cataloged(
            "legacy-model"
        )
        is False
    )
