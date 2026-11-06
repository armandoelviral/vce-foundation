from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image
from playwright.sync_api import expect

from test_inspection_observation_capture_browser import capture_ui, save
from test_inspection_observation_page_browser import live_host
from test_observation_operation_capture_browser import prepare, write_mode
from test_observation_operation_query_browser import query
from test_retail_report_jwt_composition import keys


@pytest.fixture
def photo_query(capture_ui):
    page, writer, reader, _ = capture_ui
    prepare(page, request_id="REQUEST-QUERY")
    with BytesIO() as buffer:
        with Image.new("RGB", (8, 8), "white") as image:
            image.save(buffer, format="PNG")
        original = buffer.getvalue()

    page.locator("#observation-photo").set_input_files({
        "name": "original.png",
        "mimeType": "image/png",
        "buffer": original,
    })
    save(page, writer)
    expect(page.locator("#status")).to_contain_text("Guardado confirmado")

    origin = page.url.split("/inspection-observations", 1)[0]
    page.goto(origin + "/inspection-observation-operations")
    expect(page.locator("#download-photo")).to_be_hidden()
    query(page, reader)
    expect(page.locator("#status")).to_have_text(
        "Recibo y observación recuperados."
    )
    expect(page.locator("#download-photo")).to_be_visible()
    return page, reader, original


def test_download_from_receipt_returns_original_bytes(photo_query):
    page, reader, original = photo_query
    page.locator("#credential").fill(reader)

    with page.expect_download() as pending:
        page.locator("#download-photo").click()

    download = pending.value
    assert download.failure() is None
    assert Path(download.path()).read_bytes() == original
    expect(page.locator("#photo-status")).to_have_text("Descarga iniciada.")
    expect(page.locator("#credential")).to_have_value("")
    assert reader not in page.url


@pytest.mark.parametrize("action", ["clear", "change_request"])
def test_late_photo_response_cannot_start_download(photo_query, action):
    page, reader, _ = photo_query
    downloads = []
    def record_download(download):
        downloads.append(download)

    page.on("download", record_download)

    # Hold a real authorized response after reading it. Releasing it
    # simulates a late completion even after the UI aborts the fetch.
    page.evaluate("""() => {
        const fetchOriginal = window.fetch.bind(window);
        window.fetch = async (url, options) => {
            const response = await fetchOriginal(url, options);
            if (!String(url).endsWith("/photo")) return response;
            if (response.status !== 200) throw new Error("Expected real photo");
            const blob = await response.blob();
            const copy = new Response(blob, {headers: response.headers});
            return await new Promise(resolve => {
                window.__releasePhoto = () => resolve(copy);
            });
        };
    }""")

    page.locator("#credential").fill(reader)
    page.locator("#download-photo").click()
    page.wait_for_function("() => typeof window.__releasePhoto === 'function'")
    expect(page.locator("#photo-status")).to_have_text("Recuperando foto…")

    if action == "clear":
        page.get_by_role("button", name="Limpiar", exact=True).click()
    else:
        page.locator("#request").fill("OTHER-REQUEST")

    expect(page.locator("#download-photo")).to_be_hidden()
    expect(page.locator("#output")).to_be_hidden()
    page.evaluate("""async () => {
        window.__releasePhoto();
        await new Promise(resolve =>
            requestAnimationFrame(() => requestAnimationFrame(resolve))
        );
    }""")
    expect(page.locator("#photo-status")).to_have_text("")
    expect(page.locator("#credential")).to_have_value("")
    assert downloads == []
