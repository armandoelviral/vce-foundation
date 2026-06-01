from epics.epic023_network_transport.http_transport import (
    HTTPTransport
)


transport = HTTPTransport()


ok = transport.request(
    "POST",
    "http://node-a.local/verify",
    {
        "artifact": "abc123"
    }
)


bad_method = transport.request(
    "DELETE",
    "http://node-a.local/verify",
    {}
)


bad_endpoint = transport.request(
    "POST",
    "node-a.local/verify",
    {}
)


print(
    ok["status"]
)

print(
    bad_method["status"]
)

print(
    bad_endpoint["status"]
)
