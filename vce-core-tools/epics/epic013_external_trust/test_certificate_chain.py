from certificate_chain import CertificateChain


chain = CertificateChain()


valid_cert = {
    "issuer": "github-actions",
    "subject": "repo:vce-foundation",
    "repository": "vce-core-tools",
    "expires_at": "2026-12-31"
}


bad_cert = {
    "issuer": "unknown",
    "subject": "repo:vce-foundation",
    "repository": "vce-core-tools",
    "expires_at": "2026-12-31"
}


print(
    chain.verify(valid_cert)
)

print(
    chain.verify(bad_cert)
)
