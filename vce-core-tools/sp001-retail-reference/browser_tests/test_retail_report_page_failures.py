import json

import pytest
from playwright.sync_api import expect, sync_playwright

from test_retail_report_jwt_composition import keys  # pytest fixture
from test_retail_report_page_browser import live_report_host  # pytest fixture


@pytest.fixture
def query_page(live_report_host):
    url, credential, expected_text, _ = live_report_host

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            context = browser.new_context()
            try:
                page = context.new_page()
                page.goto(url)
                yield page, credential, expected_text
            finally:
                context.close()
        finally:
            browser.close()


def submit(page, credential, report_id="REPORT-1"):
    page.locator("#case").fill("CASE")
    page.locator("#report").fill(report_id)
    page.locator("#credential").fill(credential)
    page.get_by_role("button", name="Consultar", exact=True).click()


def establish_original_report(page, credential, expected_text):
    submit(page, credential)
    expect(page.locator("#status")).to_have_text("Reporte recuperado.")
    assert page.locator("#output").text_content() == expected_text


def assert_empty_output(page):
    expect(page.locator("#output")).to_be_hidden()
    assert page.locator("#output").text_content() == ""
    expect(page.locator("#credential")).to_have_value("")
    assert page.evaluate("localStorage.length") == 0
    assert page.evaluate("sessionStorage.length") == 0


@pytest.mark.parametrize("status,body,message", [
    (
        401, {"status": "credential_rejected"},
        "Credencial rechazada o vencida.",
    ),
    (
        403, {"status": "access_denied"},
        "Acceso denegado para esta consulta.",
    ),
    (
        404, {"status": "report_not_found"},
        "Reporte no encontrado en la consulta autorizada.",
    ),
    (
        503, {"status": "backend_unavailable"},
        "No fue posible recuperar o preparar el reporte.",
    ),
    (
        404, {"detail": "Not Found"},
        "Respuesta inválida o inesperada. No se muestra un reporte.",
    ),
    (
        200, {"status": "ok", "report_text": 123},
        "Respuesta inválida o inesperada. No se muestra un reporte.",
    ),
])
def test_error_response_removes_previous_report(
    query_page, status, body, message,
):
    page, credential, expected_text = query_page
    establish_original_report(page, credential, expected_text)

    def respond(route):
        route.fulfill(
            status=status,
            content_type="application/json",
            body=json.dumps(body),
        )

    page.route("**/v1/cases/**/retail-reports/*", respond)
    submit(page, credential)

    expect(page.locator("#status")).to_have_text(message)
    assert_empty_output(page)


def test_network_failure_removes_previous_report(query_page):
    page, credential, expected_text = query_page
    establish_original_report(page, credential, expected_text)

    page.route(
        "**/v1/cases/**/retail-reports/*",
        lambda route: route.abort("failed"),
    )
    submit(page, credential)

    expect(page.locator("#status")).to_have_text(
        "No fue posible completar la consulta; revisa la conexión."
    )
    assert_empty_output(page)


def hold_first_response(page):
    # Solo en esta prueba: retener una respuesta aunque la aplicación
    # cancele la consulta. Así se prueba también la protección por generación.
    page.evaluate(r"""
        (() => {
            const originalFetch = window.fetch.bind(window);
            window.fetch = (input, options) => {
                if (!String(input).endsWith("/FIRST")) {
                    return originalFetch(input, options);
                }

                return originalFetch(
                    input, {...options, signal: undefined}
                ).then(response => new Promise(resolve => {
                    window.__releaseFirst = () => {
                        resolve(response);
                        window.__firstDelivered = true;
                    };
                    window.__firstHeld = true;
                }));
            };
        })();
    """)


@pytest.mark.parametrize("old_status,old_body", [
    (200, {"status": "ok", "report_text": "REPORTE ANTIGUO"}),
    (503, {"status": "backend_unavailable"}),
])
def test_old_response_cannot_replace_newer_result(
    query_page, old_status, old_body,
):
    page, credential, _ = query_page
    hold_first_response(page)

    def respond(route):
        if route.request.url.endswith("/FIRST"):
            status, body = old_status, old_body
        else:
            status = 200
            body = {"status": "ok", "report_text": "REPORTE RECIENTE"}

        route.fulfill(
            status=status,
            content_type="application/json",
            body=json.dumps(body),
        )

    page.route("**/v1/cases/**/retail-reports/*", respond)

    submit(page, credential, "FIRST")
    page.wait_for_function("window.__firstHeld === true")

    submit(page, credential, "SECOND")
    expect(page.locator("#output")).to_have_text("REPORTE RECIENTE")
    expect(page.locator("#status")).to_have_text("Reporte recuperado.")

    page.evaluate("window.__releaseFirst()")
    page.wait_for_function("window.__firstDelivered === true")

    expect(page.locator("#output")).to_have_text("REPORTE RECIENTE")
    expect(page.locator("#output")).to_be_visible()
    expect(page.locator("#status")).to_have_text("Reporte recuperado.")
    expect(page.locator("#credential")).to_have_value("")
    assert page.evaluate("localStorage.length") == 0
    assert page.evaluate("sessionStorage.length") == 0


def test_previous_output_is_removed_while_new_query_is_pending(query_page):
    page, credential, expected_text = query_page
    establish_original_report(page, credential, expected_text)
    hold_first_response(page)

    page.route(
        "**/v1/cases/**/retail-reports/FIRST",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({
                "status": "ok",
                "report_text": "NUEVA RESPUESTA",
            }),
        ),
    )

    submit(page, credential, "FIRST")
    page.wait_for_function("window.__firstHeld === true")

    expect(page.locator("#status")).to_have_text("Consultando…")
    assert_empty_output(page)

    page.evaluate("window.__releaseFirst()")
    expect(page.locator("#output")).to_have_text("NUEVA RESPUESTA")
    expect(page.locator("#status")).to_have_text("Reporte recuperado.")
