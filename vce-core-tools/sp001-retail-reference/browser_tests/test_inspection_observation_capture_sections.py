import pytest
from playwright.sync_api import expect

from test_inspection_observation_capture_browser import (
    capture_ui, write_mode, candidate, stored_rows, recover_http,
)
from test_inspection_observation_page_browser import live_host
from test_retail_report_jwt_composition import keys
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
)


def enter(page, values):
    for name, value in values.items():
        page.locator("#" + name).fill(value)


def next_section(page):
    page.get_by_role("button", name="Continuar", exact=True).click()


def test_first_section_shows_only_its_own_errors(capture_ui):
    page, _, _, _ = capture_ui
    expect(page.locator("#step-status")).to_have_text("Sección 1 de 4")
    expect(page.locator("#actor_id")).to_be_hidden()
    expect(page.locator("#description")).to_be_hidden()
    expect(page.locator("#credential")).to_be_hidden()
    expect(page.locator("#save")).to_be_hidden()

    next_section(page)
    expect(page.locator("#field-errors li")).to_have_count(4)
    expect(page.locator("#case_id")).to_be_focused()
    expect(page.locator("#step-status")).to_have_text("Sección 1 de 4")
    assert page.locator("#error-actor_id").count() == 0


def test_section_navigation_preserves_fields_and_can_show_full_form(capture_ui):
    page, _, _, _ = capture_ui
    enter(page, {
        "case_id": "CASE", "observation_id": "OBS-WIZARD",
        "observation_version": "1", "subject_reference": "ZONE-A",
    })
    next_section(page)
    expect(page.locator("#step-status")).to_have_text("Sección 2 de 4")
    page.locator("#actor_id").fill("DECLARED-ACTOR")
    page.get_by_role("button", name="Anterior", exact=True).click()
    expect(page.locator("#observation_id")).to_have_value("OBS-WIZARD")
    next_section(page)
    expect(page.locator("#actor_id")).to_have_value("DECLARED-ACTOR")
    page.get_by_role("button", name="Mostrar formulario completo").click()
    expect(page.locator("#description")).to_be_visible()
    expect(page.locator("#credential")).to_be_visible()
    page.get_by_role("button", name="Volver a captura por secciones").click()
    expect(page.locator("#step-status")).to_have_text("Sección 2 de 4")
    expect(page.locator("#actor_id")).to_have_value("DECLARED-ACTOR")


def test_guided_capture_saves_and_recovers_exact_document(capture_ui):
    page, token, read_token, database = capture_ui
    item = candidate()
    actor = item.declared_observer

    enter(page, {
        "case_id": item.case_id,
        "observation_id": item.observation_id,
        "observation_version": str(item.observation_version),
        "subject_reference": item.subject_reference,
    })
    next_section(page)
    enter(page, {
        "actor_id": actor.actor_id,
        "customer_id": actor.customer_id,
        "organization_id": actor.organization_id,
        "role_id": actor.role.role_id,
        "role_name": actor.role.role_name,
    })
    page.locator("#actor_type").select_option(actor.actor_type.value)
    next_section(page)
    page.locator("#method").select_option(item.method.value)
    enter(page, {
        "description": item.description,
        "scope": item.scope,
        "limitations": "\n".join(item.limitations),
        "evidence_ids": "\n".join(item.evidence_ids),
    })
    next_section(page)
    expect(page.locator("#step-status")).to_have_text("Sección 4 de 4")
    enter(page, {
        "observed_at": item.observed_at.isoformat(),
        "recorded_at": item.recorded_at.isoformat(),
        "credential": token,
    })
    page.get_by_role("button", name="Guardar", exact=True).click()
    expect(page.locator("#status")).to_contain_text("Guardado confirmado.")
    assert recover_http(page, read_token, item) == serialize(item)
    assert stored_rows(database, item.observation_id) == [
        (str(item.observation_version), serialize(item)),
    ]
    expect(page.locator("#credential")).to_have_value("")
    page.get_by_role("button", name="Anterior", exact=True).click()
    expect(page.locator("#description")).to_have_value(item.description)
