from epic010_pipeline import Epic010Pipeline

pipeline = Epic010Pipeline()

certificate = """
-----BEGIN CERTIFICATE-----
Subject: CN=urn:vce:actor:fintech-runner
-----END CERTIFICATE-----
"""

rekor_entry = {
    "uuid": {
        "verification":{}
    }
}

result = pipeline.validate(
    certificate,
    "urn:vce:actor:fintech-runner",
    rekor_entry
)

print(result)
