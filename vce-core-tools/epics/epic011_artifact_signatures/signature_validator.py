from validator import ArtifactValidator
from cryptography.exceptions import InvalidSignature


class SignatureValidator(ArtifactValidator):

    def validate(
        self,
        public_key,
        signature,
        payload
    ) -> bool:

        try:

            public_key.verify(
                signature,
                payload
            )

            return True

        except InvalidSignature:

            return False
