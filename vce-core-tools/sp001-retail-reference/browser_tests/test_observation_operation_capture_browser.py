import sqlite3
from contextlib import closing

import pytest
from playwright.sync_api import expect

import test_inspection_observation_page_browser as browser_setup
from test_inspection_observation_page_browser import live_host
from test_retail_report_jwt_composition import keys  # pytest fixture
from test_inspection_observation_capture_browser import (
    capture_ui, candidate, fill, save, retry, serialize,
)


@pytest.fixture(autouse=True)
def write_mode(monkeypatch):
    original = browser_setup.configuration
    captured = {}

    def configuration(path, keys):
        captured["database"] = path
        return {
            **original(path, keys),
            "SP001_INSPECTION_OBSERVATION_ACCESS_MODE":
                "READ_WRITE_OPERATIONS",
            "SP001_INSPECTION_OBSERVATION_MAX_REQUEST_BYTES": "1048576",
        }

    monkeypatch.setattr(browser_setup, "configuration", configuration)
    return captured


def receipts(database):
    with closing(sqlite3.connect(database)) as connection:
        return connection.execute("""
            SELECT request_id, observation_id, observation_version,
                   document, disposition
            FROM retail_observation_operations
            ORDER BY request_id
        """).fetchall()


def prepare(page, request_id="REQUEST-UI"):
    item = candidate()
    fill(page, item)
    page.locator("#request_id").fill(request_id)
    return item


def assert_token_not_stored(page, token):
    expect(page.locator("#credential")).to_have_value("")
    assert token not in page.url
    assert page.evaluate("() => localStorage.length") == 0
    assert page.evaluate("() => sessionStorage.length") == 0


def test_operation_save_and_retry_preserve_receipt(capture_ui):
    page, token, _, database = capture_ui
    item = prepare(page)
    sent = []
    page.on("request", lambda request: sent.append(
        (request.url, request.post_data)
    ) if request.method == "PUT" else None)

    save(page, token)
    expect(page.locator("#status")).to_contain_text("Guardado confirmado")
    expect(page.locator("#receipt")).to_contain_text("REQUEST-UI")
    expect(page.locator("#receipt")).to_contain_text("CREATED")
    expect(page.locator("#receipt")).to_contain_text(
        "recuperación posterior no realizada"
    )
    before = receipts(database)
    assert before == [(
        "REQUEST-UI", item.observation_id, str(item.observation_version),
        serialize(item), "CREATED",
    )]

    retry(page, token)
    expect(page.locator("#status")).to_contain_text("Guardado confirmado")
    assert len(sent) == 2
    assert sent[0] == sent[1]
    assert "/inspection-observation-operations/REQUEST-UI" in sent[0][0]
    assert sent[0][1] == serialize(item)
    assert receipts(database) == before
    assert_token_not_stored(page, token)


def test_operation_conflict_preserves_draft_and_original(capture_ui):
    page, token, _, database = capture_ui
    prepare(page)
    save(page, token)
    expect(page.locator("#status")).to_contain_text("Guardado confirmado")
    before = receipts(database)

    page.locator("#description").fill("Descripción modificada para revisión.")
    save(page, token)
    expect(page.locator("#status")).to_contain_text(
        "Conflicto: esa solicitud conserva otro contenido"
    )
    expect(page.locator("#description")).to_have_value(
        "Descripción modificada para revisión."
    )
    expect(page.locator("#request_id")).to_have_value("REQUEST-UI")
    expect(page.locator("#receipt")).to_be_hidden()
    assert receipts(database) == before
    assert_token_not_stored(page, token)


def test_lost_response_retries_original_request_and_document(capture_ui):
    page, token, _, database = capture_ui
    item = prepare(page)
    sent = []

    def lose_response(route):
        sent.append((route.request.url, route.request.post_data))
        if len(sent) == 1:
            response = route.fetch()
            assert response.status == 200
            route.abort()
        else:
            route.continue_()

    page.route("**/inspection-observation-operations/**", lose_response)
    save(page, token)
    expect(page.locator("#status")).to_contain_text("Guardado sin confirmar")
    before = receipts(database)
    assert len(before) == 1

    page.locator("#request_id").fill("EDITED-REQUEST")
    page.locator("#description").fill("Borrador posterior sin guardar.")
    save(page, token)
    expect(page.locator("#status")).to_contain_text(
        "Existe un envío sin confirmar"
    )
    assert len(sent) == 1

    retry(page, token)
    expect(page.locator("#status")).to_contain_text(
        "Envío anterior confirmado"
    )
    assert len(sent) == 2
    assert sent[0] == sent[1]
    assert sent[1][1] == serialize(item)
    assert receipts(database) == before
    expect(page.locator("#request_id")).to_have_value("EDITED-REQUEST")
    expect(page.locator("#description")).to_have_value(
        "Borrador posterior sin guardar."
    )
    assert_token_not_stored(page, token)


def test_empty_request_is_rejected_without_sending(capture_ui):
    page, token, _, database = capture_ui
    prepare(page, request_id="")
    sent = []
    page.on("request", lambda request: sent.append(request.url)
            if request.method == "PUT" else None)
    save(page, token)
    expect(page.locator("#request_id")).to_have_attribute(
        "aria-invalid", "true",
    )
    assert sent == []
    assert receipts(database) == []
    assert_token_not_stored(page, token)


def test_exact_retry_keeps_original_photo(capture_ui):
    import base64
    import json
    from io import BytesIO

    from PIL import Image

    page, writer, reader, database = capture_ui
    item = prepare(page)

    def png(color):
        with BytesIO() as output:
            with Image.new("RGB", (8, 8), color) as image:
                image.save(output, format="PNG")
            return output.getvalue()

    first_photo = png("white")
    other_photo = png("black")
    selector = page.locator("#observation-photo")
    selector.set_input_files({
        "name": "original.png", "mimeType": "image/png", "buffer": first_photo,
    })
    sent = []

    def lose_response(route):
        sent.append((
            route.request.url,
            route.request.headers["content-type"],
            route.request.post_data,
        ))
        if len(sent) == 1:
            response = route.fetch()
            assert response.status == 200
            route.abort()
        else:
            route.continue_()

    pattern = "**/inspection-observation-operations/REQUEST-UI"
    page.route(pattern, lose_response)
    save(page, writer)
    expect(page.locator("#status")).to_contain_text("Guardado sin confirmar")
    before = receipts(database)
    assert len(before) == 1

    selector.set_input_files({
        "name": "nueva.png", "mimeType": "image/png", "buffer": other_photo,
    })
    save(page, writer)
    expect(page.locator("#status")).to_contain_text("Existe un envío sin confirmar")
    assert len(sent) == 1

    retry(page, writer)
    expect(page.locator("#status")).to_contain_text("Envío anterior confirmado")
    expect(page.locator("#receipt")).to_contain_text("CREATED")
    assert len(sent) == 2 and sent[0] == sent[1]
    assert sent[0][1] == "application/vnd.sp001.observation-photo+json"
    payload = json.loads(sent[0][2])
    assert payload["observation_document"] == serialize(item)
    assert base64.b64decode(payload["photo_base64"], validate=True) == first_photo
    assert selector.evaluate("(input) => input.files[0].name") == "nueva.png"
    assert receipts(database) == before

    downloaded = page.request.get(
        sent[0][0] + "/photo",
        headers={"Authorization": "Bearer " + reader},
    )
    assert downloaded.status == 200
    assert downloaded.body() == first_photo
    assert_token_not_stored(page, writer)
