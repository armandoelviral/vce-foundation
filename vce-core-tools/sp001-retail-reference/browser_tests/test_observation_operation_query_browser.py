import json

import pytest
from playwright.sync_api import expect

from test_inspection_observation_capture_browser import (
    capture_ui, candidate, fill, save,
)
from test_inspection_observation_page_browser import live_host
from test_retail_report_jwt_composition import keys
from test_observation_operation_capture_browser import write_mode


@pytest.fixture
def operation_ui(capture_ui):
    page, write_token, read_token, _ = capture_ui
    item = candidate()
    fill(page, item)
    page.locator("#request_id").fill("REQUEST-QUERY")
    save(page, write_token)
    expect(page.locator("#status")).to_contain_text("Guardado confirmado")
    origin = page.url.split("/inspection-observations", 1)[0]
    page.goto(origin + "/inspection-observation-operations")
    yield page, read_token


def query(page, token, request_id="REQUEST-QUERY"):
    page.locator("#case").fill("CASE")
    page.locator("#request").fill(request_id)
    page.locator("#credential").fill(token)
    page.get_by_role("button", name="Consultar", exact=True).click()


def assert_empty(page):
    expect(page.locator("#output")).to_be_hidden()
    expect(page.locator("#output")).to_have_text("")
    expect(page.locator("#technical")).to_be_hidden()
    expect(page.locator("#technical-document")).to_have_text("")


def successful_query(page, token):
    query(page, token)
    expect(page.locator("#status")).to_have_text(
        "Recibo y observación recuperados."
    )


def test_recovers_receipt_and_readable_observation(operation_ui):
    page, token = operation_ui
    successful_query(page, token)
    expect(page.locator("#output")).to_contain_text("Solicitud: REQUEST-QUERY")
    expect(page.locator("#output")).to_contain_text(
        "Disposición registrada: CREATED"
    )
    expect(page.locator("#output")).to_contain_text("OBS-CAPTURE")
    expect(page.locator("#output")).to_contain_text("Versión consultada: 1")
    expect(page.locator("#output")).to_contain_text("Señal visible")
    expect(page.locator("#technical-document")).to_contain_text(
        '"schema_version":1'
    )
    expect(page.locator("#credential")).to_have_value("")
    assert token not in page.url
    assert page.evaluate(
        "() => [localStorage.length, sessionStorage.length]"
    ) == [0, 0]


@pytest.mark.parametrize("fault", [
    "case", "request", "observation", "outer_version",
    "inner_version", "disposition",
])
def test_rejects_inconsistent_pair_and_clears_previous(operation_ui, fault):
    page, token = operation_ui
    successful_query(page, token)

    def alter(route):
        response = route.fetch()
        assert response.status == 200
        body = response.json()
        if fault == "case":
            body["case_id"] = "OTHER"
        elif fault == "request":
            body["request_id"] = "OTHER"
        elif fault == "observation":
            body["observation_id"] = "OTHER"
        elif fault == "outer_version":
            body["observation_version"] = "2"
        elif fault == "inner_version":
            document = json.loads(body["observation_document"])
            document["observation"]["observation_version"] = 2
            body["observation_document"] = json.dumps(document)
        else:
            body["disposition"] = "APPROVED"
        route.fulfill(
            status=200, content_type="application/json",
            body=json.dumps(body),
        )

    page.route("**/v1/cases/*/inspection-observation-operations/*", alter)
    query(page, token)
    expect(page.locator("#status")).to_contain_text("Respuesta inválida")
    assert_empty(page)


@pytest.mark.parametrize("code,status,message", [
    (401, "credential_rejected", "Credencial rechazada"),
    (403, "access_denied", "Acceso denegado"),
    (404, "operation_not_found", "Solicitud no encontrada"),
    (503, "backend_unavailable", "No fue posible recuperar"),
    (503, "integrity_failure", "Fallo de integridad"),
])
def test_errors_clear_previous_content(operation_ui, code, status, message):
    page, token = operation_ui
    successful_query(page, token)
    page.route(
        "**/v1/cases/*/inspection-observation-operations/*",
        lambda route: route.fulfill(
            status=code, content_type="application/json",
            body=json.dumps({"status": status}),
        ),
    )
    query(page, token)
    expect(page.locator("#status")).to_contain_text(message)
    assert_empty(page)
    expect(page.locator("#credential")).to_have_value("")


def test_real_authorized_absence(operation_ui):
    page, token = operation_ui
    successful_query(page, token)
    query(page, token, "REQUEST-NOT-PRESENT")
    expect(page.locator("#status")).to_contain_text(
        "Solicitud no encontrada en la consulta autorizada."
    )
    assert_empty(page)


def hold_first_response(page):
    page.evaluate("""() => {
        const original = window.fetch.bind(window);
        let first = true;
        window.__held = false;
        window.fetch = async (...args) => {
            const response = await original(...args);
            if (first) {
                first = false;
                return await new Promise(resolve => {
                    window.__release = () => resolve(response);
                    window.__held = true;
                });
            }
            return response;
        };
    }""")


def test_clear_prevents_late_display(operation_ui):
    page, token = operation_ui
    successful_query(page, token)
    hold_first_response(page)
    query(page, token)
    page.wait_for_function("() => window.__held === true")
    page.get_by_role("button", name="Limpiar", exact=True).click()
    page.evaluate("() => window.__release()")
    # Drain fetch and rendering continuations without a fixed sleep.
    page.evaluate(
        "() => new Promise(resolve => "
        "requestAnimationFrame(() => requestAnimationFrame(resolve)))"
    )
    assert_empty(page)
    expect(page.locator("#status")).to_have_text("")


def test_late_response_cannot_replace_newer_absence(operation_ui):
    page, token = operation_ui
    hold_first_response(page)
    query(page, token)
    page.wait_for_function("() => window.__held === true")
    query(page, token, "REQUEST-NOT-PRESENT")
    expect(page.locator("#status")).to_contain_text("Solicitud no encontrada")
    page.evaluate("() => window.__release()")
    page.evaluate(
        "() => new Promise(resolve => "
        "requestAnimationFrame(() => requestAnimationFrame(resolve)))"
    )
    expect(page.locator("#status")).to_contain_text("Solicitud no encontrada")
    assert_empty(page)
