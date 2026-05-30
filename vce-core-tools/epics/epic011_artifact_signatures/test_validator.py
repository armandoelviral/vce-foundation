from signature_validator import SignatureValidator


validator = SignatureValidator()

valid_artifact = {
    "stack": {
        "trust": {
            "signature_value": "0xabc123"
        }
    }
}

invalid_artifact = {
    "stack": {
        "trust": {}
    }
}

print(
    validator.validate(valid_artifact)
)

print(
    validator.validate(invalid_artifact)
)
