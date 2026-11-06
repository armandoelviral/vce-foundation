import base64
import sqlite3
from contextlib import closing
from io import BytesIO

import pytest
from PIL import Image

import test_observation_operation_http_jwt as http
from test_retail_report_jwt_composition import keys  # pytest fixture
from sp001.infrastructure.observation_operation_http_host import PHOTO_CONTENT_TYPE


def image_bytes(format):
    with BytesIO() as output:
        with Image.new("RGB", (8, 8), "white") as image:
            image.save(output, format=format)
        return output.getvalue()


def upload(client, route, item, credential, photo):
    headers = http.headers(credential)
    headers["Content-Type"] = PHOTO_CONTENT_TYPE
    return client.put(route, headers=headers, json={
        "observation_document": http.serialize(item.observation),
        "photo_base64": base64.b64encode(photo).decode("ascii"),
    })


@pytest.mark.parametrize("format", ["JPEG", "PNG"])
def test_image_round_trip_and_exact_retry(tmp_path, keys, format):
    client, _, _, item, route = http.arrange(tmp_path, keys)
    writer = http.token(keys, http.setup.SAVE)
    reader = http.token(keys, http.setup.READ)
    photo = image_bytes(format)

    first = upload(client, route, item, writer, photo)
    assert first.status_code == 200, first.text
    assert first.json()["disposition"] == "CREATED"
    assert "observation_document" not in first.json()
    retry = upload(client, route, item, writer, photo)
    assert retry.status_code == 200
    assert retry.json() == first.json()

    denied = client.get(route + "/photo", headers=http.headers(writer))
    assert denied.status_code == 403
    result = client.get(route + "/photo", headers=http.headers(reader))
    assert result.status_code == 200
    assert result.content == photo
    assert result.headers["content-type"] == "application/octet-stream"
    assert result.headers["content-disposition"].startswith("attachment;")
    assert result.headers["cache-control"] == "no-store"
    assert result.headers["x-content-type-options"] == "nosniff"
    assert http.counts(client) == (1, 1)


@pytest.mark.parametrize("fault", ["text", "truncated_png", "gif"])
def test_invalid_image_leaves_no_effect(tmp_path, keys, fault):
    client, _, _, item, route = http.arrange(tmp_path, keys)
    writer = http.token(keys, http.setup.SAVE)
    photo = {
        "text": b"not an image",
        "truncated_png": image_bytes("PNG")[:40],
        "gif": image_bytes("GIF"),
    }[fault]

    result = upload(client, route, item, writer, photo)
    assert result.status_code == 400
    assert result.json() == {"status": "invalid_photo"}
    assert http.counts(client) == (0, 0)
    with closing(sqlite3.connect(client.app.state.operation_database)) as db:
        assert db.execute(
            "SELECT COUNT(*) FROM retail_observation_photos"
        ).fetchone() == (0,)


def test_revoked_reader_cannot_download_with_same_token(tmp_path, keys):
    client, _, _, item, route = http.arrange(tmp_path, keys)
    writer = http.token(keys, http.setup.SAVE)
    read_headers = http.headers(http.token(keys, http.setup.READ))
    assert upload(client, route, item, writer, image_bytes("PNG")).status_code == 200
    assert client.get(route + "/photo", headers=read_headers).status_code == 200

    # Change the grant consulted by the backend, without changing the JWT.
    with closing(sqlite3.connect(client.app.state.operation_database)) as db:
        changed = db.execute(
            "UPDATE case_access_grants SET revoked=1 "
            "WHERE case_id=? AND operation=? AND revoked=0",
            (item.observation.case_id, http.setup.READ.value),
        )
        assert changed.rowcount == 1
        db.commit()

    result = client.get(route + "/photo", headers=read_headers)
    assert result.status_code == 403
    assert result.json() == {"status": "access_denied"}
    assert http.counts(client) == (1, 1)


def test_corrupt_photo_is_not_served(tmp_path, keys):
    client, _, _, item, route = http.arrange(tmp_path, keys)
    writer = http.token(keys, http.setup.SAVE)
    reader = http.token(keys, http.setup.READ)
    assert upload(client, route, item, writer, image_bytes("PNG")).status_code == 200
    with closing(sqlite3.connect(client.app.state.operation_database)) as db:
        db.execute("UPDATE retail_observation_photos SET content=X'00'")
        db.commit()

    result = client.get(route + "/photo", headers=http.headers(reader))
    assert result.status_code == 503
    assert result.json() == {"status": "integrity_failure"}
    assert "content-disposition" not in result.headers
