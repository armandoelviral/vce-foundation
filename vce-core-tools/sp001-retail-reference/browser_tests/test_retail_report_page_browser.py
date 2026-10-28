import asyncio
import socket
import threading
import time

import pytest
import uvicorn
from playwright.sync_api import expect, sync_playwright

import test_retail_report_jwt_composition as setup
from test_retail_report_jwt_composition import keys  # pytest fixture
from test_retail_report_host_bootstrap import configuration

from sp001.infrastructure.retail_report_host_bootstrap import (
    create_app_from_environment,
)
from sp001.services.retail_vm_report_text import render_retail_vm_report_text


@pytest.fixture
def live_report_host(tmp_path, keys):
    database, service, _, _ = setup.environment(tmp_path, keys)
    credential = setup.token(keys[0])
    report = setup.make_report()

    service.save(
        credential=credential,
        identity=setup.IDENTITY,
        report=report,
    )

    recovered = service.recover_with_admissions(
        credential=credential,
        identity=setup.IDENTITY,
        case_id="CASE",
    )
    expected_text = render_retail_vm_report_text(
        identity=setup.IDENTITY,
        recovered=recovered,
    )

    app = create_app_from_environment(
        environment=configuration(database, keys),
    )

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))
    port = listener.getsockname()[1]

    server = uvicorn.Server(uvicorn.Config(
        app,
        host="127.0.0.1",
        port=port,
        lifespan="off",
        loop="asyncio",
        access_log=False,
        log_level="critical",
        timeout_graceful_shutdown=1,
    ))
    failures = []

    def run():
        try:
            asyncio.run(server.serve(sockets=[listener]))
        except BaseException as error:
            failures.append(error)

    thread = threading.Thread(target=run, daemon=True)

    try:
        thread.start()
        deadline = time.monotonic() + 10

        while not server.started and thread.is_alive():
            if time.monotonic() >= deadline:
                pytest.fail("El host no inició dentro del plazo")
            time.sleep(0.01)

        if failures:
            raise failures[0]
        if not server.started:
            pytest.fail("El host terminó antes de iniciar")

        yield (
            f"http://127.0.0.1:{port}/retail-reports",
            credential,
            expected_text,
            database,
        )
    finally:
        server.should_exit = True
        thread.join(timeout=5)
        listener.close()
        if thread.is_alive():
            pytest.fail("El host no terminó dentro del plazo")


def test_browser_reads_report_and_clears_it_after_rejection(live_report_host):
    url, credential, expected_text, database = live_report_host

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            context = browser.new_context()
            try:
                page = context.new_page()
                page.goto(url)

                page.locator("#case").fill("CASE")
                page.locator("#report").fill("REPORT-1")
                page.locator("#credential").fill(credential)
                page.get_by_role(
                    "button", name="Consultar", exact=True,
                ).click()

                expect(page.locator("#status")).to_have_text(
                    "Reporte recuperado."
                )
                expect(page.locator("#output")).to_be_visible()
                assert page.locator("#output").text_content() == expected_text
                expect(page.locator("#credential")).to_have_value("")

                # Contexto nuevo: la aplicación no debe escribir datos
                # en ninguno de estos dos almacenes.
                assert page.evaluate("localStorage.length") == 0
                assert page.evaluate("sessionStorage.length") == 0
                assert credential not in page.url

                # Una consulta posterior rechazada elimina la salida previa.
                page.locator("#credential").fill("invalid-credential")
                page.get_by_role(
                    "button", name="Consultar", exact=True,
                ).click()

                expect(page.locator("#status")).to_have_text(
                    "Credencial rechazada o vencida."
                )
                expect(page.locator("#output")).to_be_hidden()
                assert page.locator("#output").text_content() == ""
                expect(page.locator("#credential")).to_have_value("")

                assert page.evaluate("localStorage.length") == 0
                assert page.evaluate("sessionStorage.length") == 0
                assert setup.row_count(database) == 1
            finally:
                context.close()
        finally:
            browser.close()
