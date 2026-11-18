import os
import socket
import subprocess
import sys
import time
import urllib.request

import pytest


APP = "sp001.infrastructure.product001_host_bootstrap:create_app"


def free_loopback_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def start_host(mode, port, overrides=None):
    environment = dict(os.environ)
    environment["PRODUCT001_ENV"] = mode

    if overrides:
        environment.update(overrides)

    command = [
        sys.executable,
        "-m",
        "uvicorn",
        APP,
        "--factory",
        "--host",
        "127.0.0.1",
        "--port",
        str(port),
        "--no-access-log",
    ]

    return subprocess.Popen(
        command,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def stop_host(process):
    if process.poll() is None:
        process.terminate()

    try:
        output, _ = process.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        output, _ = process.communicate(timeout=5)

    return output


@pytest.mark.parametrize(
    "mode,overrides",
    [
        ("production", {}),
        ("commercial", {}),
        ("staging-commercial", {}),
        (
            "production",
            {
                "BLOCKER_HOST_001_OPEN": "false",
                "TRUST_ROOT_VERIFIED": "true",
            },
        ),
    ],
)
def test_commercial_host_cannot_start(mode, overrides):
    port = free_loopback_port()
    process = start_host(mode, port, overrides)

    try:
        output, _ = process.communicate(timeout=10)

        assert process.returncode != 0
        assert "CommercialStartupBlockedError" in output
        assert "BLOCKER-HOST-001" in output

        with socket.socket() as sock:
            sock.settimeout(0.5)
            assert sock.connect_ex(
                ("127.0.0.1", port)
            ) != 0

    finally:
        stop_host(process)


def test_laboratory_host_accepts_http():
    port = free_loopback_port()
    process = start_host("laboratory", port)

    try:
        deadline = time.monotonic() + 10
        response = None

        while time.monotonic() < deadline:
            if process.poll() is not None:
                break

            try:
                with urllib.request.urlopen(
                    f"http://127.0.0.1:{port}/openapi.json",
                    timeout=0.5,
                ) as result:
                    response = (
                        result.status,
                        result.read(),
                    )
                break

            except (
                OSError,
                TimeoutError,
            ):
                time.sleep(0.1)

        assert response is not None
        assert response[0] == 200
        assert b"PRODUCT-001 Laboratory Host" in response[1]

    finally:
        stop_host(process)
