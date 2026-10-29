from dataclasses import replace
from datetime import datetime, timedelta, timezone
import sqlite3

import pytest
from playwright.sync_api import sync_playwright, expect

import test_inspection_observation_page_browser as browser_setup
from test_inspection_observation_page_browser import live_host
from test_retail_report_jwt_composition import keys
import test_retail_report_jwt_composition as jwt_setup
from test_retail_inspection_observation import observation
from sp001.contracts.case_access_context import CaseAccessOperation as Operation
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
    deserialize_retail_inspection_observation as deserialize,
)


API = "**/v1/cases/*/inspection-observations/*/versions/*"


@pytest.fixture(autouse=True)
def write_mode(monkeypatch):
    original = browser_setup.configuration
    captured = {}

    def configuration(path, keys):
        captured["database"] = path
        return {
            **original(path, keys),
            "SP001_INSPECTION_OBSERVATION_ACCESS_MODE": "READ_WRITE",
            "SP001_INSPECTION_OBSERVATION_MAX_REQUEST_BYTES": "1048576",
        }

    monkeypatch.setattr(browser_setup, "configuration", configuration)
    return captured


@pytest.fixture
def capture_ui(live_host, keys, write_mode):
    url, read_token, _ = live_host
    write_token = jwt_setup.token(
        keys[0], operations=(Operation.SAVE_RETAIL_OBSERVATION,),
    )
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto(url + "/capture")
            # Emit credentials after browser startup and page readiness.
            write_token = jwt_setup.token(
                keys[0], operations=(Operation.SAVE_RETAIL_OBSERVATION,),
            )
            read_token = jwt_setup.token(
                keys[0], operations=(Operation.READ_RETAIL_OBSERVATION,),
            )
            yield page, write_token, read_token, write_mode["database"]
        finally:
            page.on("dialog", lambda dialog: dialog.dismiss())
            context.close()
            browser.close()


def candidate(version=1):
    instant = datetime(
        2026, 1, 1, 12, 30, 10, 123456,
        tzinfo=timezone(timedelta(hours=-6)),
    )
    return observation(
        observation_id="OBS-CAPTURE", observation_version=version,
        case_id="CASE",
        description="  Señal visible: á, ñ, 漢字, 😀\nSegunda línea.  ",
        scope="Frente visible; sin inspección física.",
        limitations=("No se midió.", "Zona posterior oculta."),
        evidence_ids=("PHOTO-2", "PHOTO-1"),
        observed_at=instant,
        recorded_at=instant + timedelta(minutes=1),
    )


def fill(page, item):
    mode = page.locator("#view-mode")
    if mode.text_content() == "Mostrar formulario completo":
        mode.click()
    actor = item.declared_observer
    values = {
        "case_id": item.case_id,
        "observation_id": item.observation_id,
        "observation_version": str(item.observation_version),
        "subject_reference": item.subject_reference,
        "actor_id": actor.actor_id,
        "customer_id": actor.customer_id,
        "organization_id": actor.organization_id,
        "role_id": actor.role.role_id,
        "role_name": actor.role.role_name,
        "observed_at": item.observed_at.isoformat(),
        "recorded_at": item.recorded_at.isoformat(),
        "description": item.description,
        "scope": item.scope,
        "limitations": "\n".join(item.limitations),
        "evidence_ids": "\n".join(item.evidence_ids),
    }
    for name, value in values.items():
        page.locator("#" + name).fill(value)
    page.locator("#method").select_option(item.method.value)
    page.locator("#actor_type").select_option(actor.actor_type.value)


def save(page, token):
    page.locator("#credential").fill(token)
    page.get_by_role("button", name="Guardar", exact=True).click()


def retry(page, token):
    page.locator("#credential").fill(token)
    page.get_by_role(
        "button", name="Reintentar envío exacto", exact=True,
    ).click()


def stored_rows(database, observation_id):
    with sqlite3.connect(database) as connection:
        return connection.execute("""
            SELECT observation_version, document
            FROM retail_inspection_observations WHERE observation_id=?
        """, (observation_id,)).fetchall()


def recover_http(page, read_token, item):
    route = (
        "/v1/cases/CASE/inspection-observations/"
        + item.observation_id + "/versions/" + str(item.observation_version)
    )
    response = page.request.get(
        page.url.split("/inspection-observations", 1)[0] + route,
        headers={"Authorization": "Bearer " + read_token},
    )
    assert response.status == 200
    return response.json()["observation_document"]


def assert_no_token_storage(page, token):
    expect(page.locator("#credential")).to_have_value("")
    assert token not in page.url
    assert page.evaluate("() => localStorage.length") == 0
    assert page.evaluate("() => sessionStorage.length") == 0


@pytest.mark.parametrize("version", [1, 2**60 + 1])
def test_browser_document_matches_python_codec_and_roundtrips(
    capture_ui, version,
):
    page, write_token, read_token, database = capture_ui
    item = candidate(version)
    fill(page, item)

    with page.expect_request(
        lambda request: request.method == "PUT",
    ) as outgoing:
        save(page, write_token)

    expect(page.locator("#status")).to_contain_text("Guardado confirmado.")
    sent = outgoing.value.post_data
    assert sent == serialize(item)
    assert deserialize(sent) == item
    assert recover_http(page, read_token, item) == sent
    assert stored_rows(database, item.observation_id) == [
        (str(version), sent),
    ]
    expect(page.locator("#description")).to_have_value(item.description)
    expect(page.locator("#observation_version")).to_have_value(str(version))
    assert_no_token_storage(page, write_token)


def test_response_lost_after_commit_retries_exact_original_with_one_row(capture_ui):
    page, write_token, read_token, database = capture_ui
    item = candidate()
    fill(page, item)
    sent_documents = []

    def lose_first_response(route):
        sent_documents.append(route.request.post_data)
        response = route.fetch()
        assert response.status == 200
        route.abort("failed")

    page.route(API, lose_first_response, times=1)
    save(page, write_token)
    expect(page.locator("#status")).to_contain_text("Guardado sin confirmar")
    expect(page.locator("#description")).to_have_value(item.description)
    assert stored_rows(database, item.observation_id) == [
        ("1", serialize(item)),
    ]
    assert_no_token_storage(page, write_token)

    # An edit must not silently replace the uncertain request.
    edited = "Cambios locales todavía no guardados."
    page.locator("#description").fill(edited)
    save(page, write_token)
    expect(page.locator("#status")).to_contain_text(
        "Existe un envío sin confirmar."
    )
    assert len(sent_documents) == 1

    with page.expect_request(
        lambda request: request.method == "PUT",
    ) as outgoing:
        retry(page, write_token)

    expect(page.locator("#status")).to_contain_text(
        "Envío anterior confirmado."
    )
    assert outgoing.value.post_data == sent_documents[0] == serialize(item)
    expect(page.locator("#description")).to_have_value(edited)
    assert recover_http(page, read_token, item) == serialize(item)
    assert stored_rows(database, item.observation_id) == [
        ("1", serialize(item)),
    ]
    assert_no_token_storage(page, write_token)


def test_conflict_preserves_draft_and_does_not_increment_version(capture_ui):
    page, write_token, read_token, database = capture_ui
    original = candidate()
    fill(page, original)
    save(page, write_token)
    expect(page.locator("#status")).to_contain_text("Guardado confirmado.")

    changed = "Descripción contradictoria bajo la misma versión."
    page.locator("#description").fill(changed)
    save(page, write_token)
    expect(page.locator("#status")).to_contain_text("Conflicto:")
    expect(page.locator("#description")).to_have_value(changed)
    expect(page.locator("#observation_version")).to_have_value("1")
    expect(page.locator("#receipt")).to_be_hidden()
    assert recover_http(page, read_token, original) == serialize(original)
    assert stored_rows(database, original.observation_id) == [
        ("1", serialize(original)),
    ]


def test_denied_save_preserves_draft_and_never_creates_record(capture_ui):
    page, _, read_token, database = capture_ui
    item = candidate()
    fill(page, item)
    save(page, read_token)
    expect(page.locator("#status")).to_contain_text("Acceso denegado.")
    expect(page.locator("#status")).to_contain_text("Guardado sin confirmar")
    expect(page.locator("#description")).to_have_value(item.description)
    expect(page.locator("#observation_version")).to_have_value("1")
    assert stored_rows(database, item.observation_id) == []
    assert_no_token_storage(page, read_token)
