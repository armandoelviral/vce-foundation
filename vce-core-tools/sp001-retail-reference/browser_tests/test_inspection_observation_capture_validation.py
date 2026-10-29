import pytest
from playwright.sync_api import expect

from test_inspection_observation_capture_browser import (
    capture_ui, write_mode, candidate, fill, save, stored_rows,
)
from test_inspection_observation_page_browser import live_host
from test_retail_report_jwt_composition import keys


def watch_puts(page):
    requests = []
    page.on("request", lambda request:
        requests.append(request) if request.method == "PUT" else None
    )
    return requests


def test_missing_field_identifies_and_focuses_it_without_losing_draft(capture_ui):
    page, token, _, database = capture_ui
    item = candidate()
    fill(page, item)
    page.locator("#subject_reference").fill("")
    requests = watch_puts(page)
    save(page, token)

    expect(page.locator("#error-subject_reference")).to_have_text(
        "Objeto o zona observada: Completa este campo."
    )
    expect(page.locator("#subject_reference")).to_be_focused()
    expect(page.locator("#subject_reference")).to_have_attribute(
        "aria-invalid", "true"
    )
    expect(page.locator("#description")).to_have_value(item.description)
    expect(page.locator("#credential")).to_have_value("")
    assert requests == []
    assert stored_rows(database, item.observation_id) == []

    page.locator("#subject_reference").fill(item.subject_reference)
    save(page, token)
    expect(page.locator("#status")).to_contain_text("Guardado confirmado.")
    expect(page.locator("#field-errors")).to_be_hidden()
    expect(page.locator("#subject_reference")).not_to_have_attribute(
        "aria-invalid", "true"
    )


@pytest.mark.parametrize("reference", ["----", "...", "???", "   "])
def test_marker_only_reference_is_rejected_without_sending(capture_ui, reference):
    page, token, _, database = capture_ui
    item = candidate()
    fill(page, item)
    page.locator("#evidence_ids").fill(reference)
    requests = watch_puts(page)
    save(page, token)

    expect(page.locator("#error-evidence_ids")).to_contain_text(
        "no uses solo signos"
    )
    expect(page.locator("#evidence_ids")).to_be_focused()
    expect(page.locator("#evidence_ids")).to_have_value(reference)
    expect(page.locator("#description")).to_have_value(item.description)
    assert requests == []
    assert stored_rows(database, item.observation_id) == []


@pytest.mark.parametrize("value", [
    "2026-02-30T12:00:00-06:00",
    "2026-10-29T12:00:00",
    "2026-10-29T25:00:00-06:00",
])
def test_invalid_date_identifies_field_and_preserves_input(capture_ui, value):
    page, token, _, _ = capture_ui
    fill(page, candidate())
    page.locator("#observed_at").fill(value)
    requests = watch_puts(page)
    save(page, token)
    expect(page.locator("#error-observed_at")).to_contain_text("fecha válida")
    expect(page.locator("#observed_at")).to_have_value(value)
    assert requests == []


def test_recording_before_observation_is_explained(capture_ui):
    page, token, _, _ = capture_ui
    fill(page, candidate())
    page.locator("#recorded_at").fill("2025-01-01T12:00:00-06:00")
    requests = watch_puts(page)
    save(page, token)
    expect(page.locator("#error-recorded_at")).to_contain_text(
        "No puede ser anterior"
    )
    assert requests == []


def test_duplicate_reference_is_explained(capture_ui):
    page, token, _, _ = capture_ui
    fill(page, candidate())
    page.locator("#evidence_ids").fill("PHOTO-1\nPHOTO-1")
    requests = watch_puts(page)
    save(page, token)
    expect(page.locator("#error-evidence_ids")).to_contain_text("duplicadas")
    assert requests == []


def test_evidence_review_requires_a_reference(capture_ui):
    page, token, _, _ = capture_ui
    fill(page, candidate())
    page.locator("#evidence_ids").fill("")
    requests = watch_puts(page)
    save(page, token)
    expect(page.locator("#error-evidence_ids")).to_contain_text(
        "al menos una referencia"
    )
    assert requests == []


def test_missing_credential_is_identified(capture_ui):
    page, _, _, _ = capture_ui
    fill(page, candidate())
    requests = watch_puts(page)
    save(page, "")
    expect(page.locator("#error-credential")).to_contain_text(
        "Pega la clave de acceso"
    )
    expect(page.locator("#credential")).to_be_focused()
    assert requests == []
