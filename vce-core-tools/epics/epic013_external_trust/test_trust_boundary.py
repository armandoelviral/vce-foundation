from trust_boundary import TrustBoundary

boundary = TrustBoundary(
    allowed_issuers=[
        "github-actions"
    ]
)

valid = {
    "issuer": "github-actions",
    "signature_valid": True
}

invalid = {
    "issuer": "unknown-runner",
    "signature_valid": True
}

tampered = {
    "issuer": "github-actions",
    "signature_valid": False
}

print(boundary.verify(valid))
print(boundary.verify(invalid))
print(boundary.verify(tampered))
