import pytest
from playwright.sync_api import expect, sync_playwright

from test_retail_report_jwt_composition import keys  # pytest fixture
from test_retail_report_page_browser import live_report_host  # pytest fixture


@pytest.mark.parametrize(
    ("live_report_host", "expected_admissions"),
    [("declared", 0), ("recorded", 1)],
    indirect=["live_report_host"],
)
def test_browser_distinguishes_declared_and_recorded_attribution(
    live_report_host, expected_admissions,
):
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
                text = page.locator("#output").text_content()

                assert text == expected_text
                assert "La admisión no equivale a aprobación" in text
                assert "La admisión no demuestra revisión independiente." in text
                assert "Resultado declarado: CONFORMANT" in text
                assert "Synthetic rationale." in text

                # Corroborar cuál fue la ruta usada en la base temporal.
                import sqlite3
                with sqlite3.connect(database) as connection:
                    admission_count = connection.execute(
                        "SELECT COUNT(*) FROM retail_evaluation_admissions"
                    ).fetchone()[0]

                assert admission_count == expected_admissions

                if expected_admissions == 0:
                    assert (
                        "Atribución: DECLARADA; sin admisión local recuperada."
                    ) in text
                    assert "Atribución: ADMISIÓN LOCAL REGISTRADA." not in text
                    assert "Sujeto del principal:" not in text
                else:
                    assert admission_count == 1
                    assert "Atribución: ADMISIÓN LOCAL REGISTRADA." in text
                    assert "Atribución: DECLARADA;" not in text
                    assert 'Sujeto del principal: "SUBJECT"' in text
                    assert 'Vinculación: "BROWSER-BINDING"' in text
                    assert "Revisión utilizada: 1" in text

                expect(page.locator("#credential")).to_have_value("")
                assert page.evaluate("localStorage.length") == 0
                assert page.evaluate("sessionStorage.length") == 0
            finally:
                context.close()
        finally:
            browser.close()
