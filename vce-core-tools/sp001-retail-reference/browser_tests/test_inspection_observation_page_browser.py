import asyncio
import json
import socket
from threading import Thread
import time

import pytest
import uvicorn
from playwright.sync_api import sync_playwright, expect

import test_authenticated_inspection_observations_jwt as setup
import test_retail_report_jwt_composition as jwt_setup
from test_retail_report_jwt_composition import keys
from test_inspection_observation_host_bootstrap import configuration
from sp001.infrastructure.inspection_observation_host_bootstrap import (
    create_app_from_environment,
)
from sp001.infrastructure.retail_inspection_observation_serialization import (
    serialize_retail_inspection_observation as serialize,
)


API = "**/v1/cases/*/inspection-observations/*/versions/*"


@pytest.fixture
def live_host(tmp_path, keys):
    database, service, _, _, _ = setup.environment(tmp_path, keys)
    item = setup.observation(case_id=setup.CASE)
    service.save(
        credential=jwt_setup.token(keys[0], operations=(setup.SAVE,)),
        observation=item,
    )
    credential = jwt_setup.token(keys[0], operations=(setup.READ,))
    app = create_app_from_environment(
        environment=configuration(database, keys),
    )
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))
    listener.listen(128)
    port = listener.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(
        app, log_level="warning", access_log=False, lifespan="off",
    ))
    errors = []

    def run():
        try:
            asyncio.run(server.serve(sockets=[listener]))
        except BaseException as error:
            errors.append(error)

    thread = Thread(target=run, daemon=True)
    thread.start()
    try:
        deadline = time.monotonic() + 10
        while not server.started:
            if errors:
                raise errors[0]
            if not thread.is_alive():
                raise AssertionError("host exited before readiness")
            if time.monotonic() >= deadline:
                raise AssertionError("host readiness timeout")
            time.sleep(0.02)
        yield (
            f"http://127.0.0.1:{port}/inspection-observations",
            credential, serialize(item),
        )
    finally:
        server.should_exit = True
        thread.join(timeout=5)
        if thread.is_alive():
            server.force_exit = True
            thread.join(timeout=5)
        listener.close()
        assert not thread.is_alive(), "host did not terminate"
        if errors:
            raise errors[0]


@pytest.fixture
def ui(live_host):
    url, token, document = live_host
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto(url)
            yield page, token, document
        finally:
            context.close()
            browser.close()


def query(page, token, observation_id="OBS-1"):
    page.locator("#case").fill("CASE")
    page.locator("#observation").fill(observation_id)
    page.locator("#version").fill("1")
    page.locator("#credential").fill(token)
    page.get_by_role("button", name="Consultar", exact=True).click()


def assert_no_token_storage(page, token):
    expect(page.locator("#credential")).to_have_value("")
    assert token not in page.url
    assert page.evaluate("localStorage.length") == 0
    assert page.evaluate("sessionStorage.length") == 0


def assert_empty(page):
    expect(page.locator("#output")).to_be_hidden()
    expect(page.locator("#output")).to_have_text("")
    expect(page.locator("#technical")).to_be_hidden()
    expect(page.locator("#technical-document")).to_have_text("")


def successful_query(page, token, document):
    query(page, token)
    expect(page.locator("#status")).to_have_text("Observación recuperada.")
    expect(page.locator("#output")).to_be_visible()
    original = json.loads(document)["observation"]
    text = page.locator("#output").text_content()
    assert original["description"] in text
    assert original["scope"] in text
    assert "SIN DICTAMEN" in text
    assert "Responsable declarado" in text
    assert document not in text
    assert page.locator("#technical-document").text_content() == document
    expect(page.locator("#technical-document")).to_be_hidden()
    assert_no_token_storage(page, token)


def test_real_authorized_query_and_rejected_credential_clear_content(ui):
    page, token, document = ui
    successful_query(page, token, document)
    query(page, "invalid-credential")
    expect(page.locator("#status")).to_have_text(
        "Credencial rechazada o vencida."
    )
    assert_empty(page)
    assert_no_token_storage(page, token)


@pytest.mark.parametrize("code,body,message", [
    (400, {"status": "invalid_request"}, "Datos de consulta inválidos."),
    (401, {"status": "credential_rejected"}, "Credencial rechazada o vencida."),
    (403, {"status": "access_denied"}, "Acceso denegado para esta consulta."),
    (404, {"status": "observation_not_found"},
     "Observación no encontrada en la consulta autorizada."),
    (503, {"status": "backend_unavailable"},
     "No fue posible recuperar o preparar la observación."),
    (404, {"detail": "infrastructure route missing"},
     "Respuesta inválida; no se muestra una observación."),
    (200, {"status": "ok", "observation_document": 123},
     "Respuesta inválida; no se muestra una observación."),
])
def test_error_responses_remove_previous_content(ui, code, body, message):
    page, token, document = ui
    successful_query(page, token, document)
    page.route(API, lambda route: route.fulfill(
        status=code, content_type="application/json", body=json.dumps(body),
    ))
    query(page, token)
    expect(page.locator("#status")).to_have_text(message)
    assert_empty(page)
    assert_no_token_storage(page, token)


def test_network_failure_clears_content(ui):
    page, token, document = ui
    successful_query(page, token, document)
    page.route(API, lambda route: route.abort("failed"))
    query(page, token)
    expect(page.locator("#status")).to_have_text(
        "No fue posible completar la consulta; revisa la conexión."
    )
    assert_empty(page)
    assert_no_token_storage(page, token)


def test_invalid_json_clears_content(ui):
    page, token, document = ui
    successful_query(page, token, document)
    page.route(API, lambda route: route.fulfill(
        status=200, content_type="application/json", body="{invalid",
    ))
    query(page, token)
    expect(page.locator("#status")).to_have_text(
        "Respuesta inválida; no se muestra una observación."
    )
    assert_empty(page)


def hold_first_response(page):
    # Ignore cancellation only for the first request, so the generation
    # guard must withstand a response that still reaches JavaScript.
    page.evaluate(r"""() => {
        const original = window.fetch.bind(window);
        let first = true;
        window.__held = false;
        window.__delivered = false;
        window.fetch = async (url, options) => {
            if (!first) return original(url, options);
            first = false;
            const response = await original(url, {...options, signal: undefined});
            await new Promise(resolve => {
                window.__release = resolve;
                window.__held = true;
            });
            window.__delivered = true;
            return response;
        };
    }""")


@pytest.mark.parametrize("old_status", [200, 503])
def test_stale_response_cannot_replace_newer_result(ui, old_status):
    page, token, document = ui
    successful_query(page, token, document)
    hold_first_response(page)

    def respond(route):
        old = "/OLD/" in route.request.url
        if old and old_status == 503:
            payload = {"status": "backend_unavailable"}
        else:
            envelope = json.loads(document)
            item = envelope["observation"]
            item["observation_id"] = "OLD" if old else "LATEST"
            item["description"] = "OLD CONTENT" if old else "LATEST CONTENT"
            payload = {
                "status": "ok",
                "observation_document": json.dumps(envelope),
            }
        route.fulfill(
            status=old_status if old else 200,
            content_type="application/json", body=json.dumps(payload),
        )

    page.route(API, respond)
    query(page, token, "OLD")
    page.wait_for_function("() => window.__held === true")
    assert_empty(page)

    query(page, token, "LATEST")
    expect(page.locator("#status")).to_have_text("Observación recuperada.")
    expect(page.locator("#output")).to_contain_text("LATEST CONTENT")
    current_document = page.locator("#technical-document").text_content()

    page.evaluate("window.__release()")
    page.wait_for_function("() => window.__delivered === true")
    page.evaluate("() => new Promise(resolve => setTimeout(resolve, 0))")
    expect(page.locator("#output")).to_contain_text("LATEST CONTENT")
    expect(page.locator("#output")).not_to_contain_text("OLD CONTENT")
    assert page.locator("#technical-document").text_content() == current_document
    expect(page.locator("#status")).to_have_text("Observación recuperada.")
    assert_no_token_storage(page, token)


def test_clear_during_pending_query_prevents_late_display(ui):
    page, token, document = ui
    successful_query(page, token, document)
    hold_first_response(page)
    query(page, token)
    page.wait_for_function("() => window.__held === true")
    assert_empty(page)

    page.get_by_role("button", name="Limpiar", exact=True).click()
    page.evaluate("window.__release()")
    page.wait_for_function("() => window.__delivered === true")
    page.evaluate("() => new Promise(resolve => setTimeout(resolve, 0))")

    assert_empty(page)
    expect(page.locator("#status")).to_have_text("")
    for field in ("case", "observation", "version", "credential"):
        expect(page.locator("#" + field)).to_have_value("")
    assert_no_token_storage(page, token)


def test_document_is_rendered_as_text_not_html(ui):
    page, token, document = ui
    literal = '<img id="injected" src=x onerror="window.__injected=true">'
    envelope = json.loads(document)
    envelope["observation"]["description"] = literal
    changed = json.dumps(envelope)
    page.route(API, lambda route: route.fulfill(
        status=200, content_type="application/json",
        body=json.dumps({"status": "ok", "observation_document": changed}),
    ))
    query(page, token)
    expect(page.locator("#status")).to_have_text("Observación recuperada.")
    expect(page.locator("#output")).to_contain_text(literal)
    assert page.locator("#technical-document").text_content() == changed
    assert page.locator("#injected").count() == 0
    assert page.evaluate("() => window.__injected === true") is False


def test_readable_fields_preserve_literals_and_original_document(ui):
    page, token, document = ui
    envelope = json.loads(document)
    item = envelope["observation"]
    item["description"] = "NO SE RESPETA LINEAMIENTO — declaración sin validar."
    item["scope"] = "  Zona frontal\nSin revisar parte posterior.  "
    item["limitations"]["items"] = ["Sin medición.", "Zona oculta."]
    item["evidence_ids"]["items"] = ["PHOTO-1", "----"]
    item["declared_observer"]["fields"]["role"]["fields"]["role_name"] = "Revisor ñ"
    changed = json.dumps(envelope, ensure_ascii=True)
    page.route(API, lambda route: route.fulfill(
        status=200, content_type="application/json",
        body=json.dumps({"status": "ok", "observation_document": changed}),
    ))
    query(page, token)
    expect(page.locator("#status")).to_have_text("Observación recuperada.")
    text = page.locator("#output").text_content()
    for literal in (
        item["description"], item["scope"], "Sin medición.", "Zona oculta.",
        "PHOTO-1", "----", "Revisor ñ", item["observed_at"]["iso"],
        item["recorded_at"]["iso"], "No se ha clasificado",
    ):
        assert literal in text
    assert page.locator("#technical-document").text_content() == changed
    page.locator("#technical summary").click()
    expect(page.locator("#technical-document")).to_be_visible()


def test_readable_version_uses_exact_decimal_without_js_rounding(ui):
    page, token, document = ui
    version = 2**60 + 1
    envelope = json.loads(document)
    envelope["observation"]["observation_version"] = version
    changed = json.dumps(envelope)
    page.route(API, lambda route: route.fulfill(
        status=200, content_type="application/json",
        body=json.dumps({"status": "ok", "observation_document": changed}),
    ))
    page.locator("#case").fill("CASE")
    page.locator("#observation").fill("OBS-1")
    page.locator("#version").fill(str(version))
    page.locator("#credential").fill(token)
    page.get_by_role("button", name="Consultar", exact=True).click()
    expect(page.locator("#status")).to_have_text("Observación recuperada.")
    expect(page.locator("#output")).to_contain_text(
        "Versión consultada: " + str(version)
    )
    assert page.locator("#technical-document").text_content() == changed


def test_malformed_embedded_document_clears_both_views(ui):
    page, token, document = ui
    successful_query(page, token, document)
    page.route(API, lambda route: route.fulfill(
        status=200, content_type="application/json",
        body=json.dumps({"status": "ok", "observation_document": "{}"}),
    ))
    query(page, token)
    expect(page.locator("#status")).to_have_text(
        "Respuesta inválida; no se muestra una observación."
    )
    assert_empty(page)
