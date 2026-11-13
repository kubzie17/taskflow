"""Optional infrastructure. Use only the pool, client and group names you configured."""
import os
from urllib.parse import urlsplit

import jwt

from exercises.day05_api import create_secure
from exercises.day05_identity import InvalidCredential, Principal


class CognitoIdentity:
    def __init__(self, issuer: str, client_id: str, resource: str, key_source=None):
        if not all((issuer, client_id, resource)):
            raise ValueError("Set a pool issuer, public app client ID and API resource URI.")
        if not issuer.startswith("https://") or not resource.startswith("https://"):
            raise ValueError("The issuer and resource identifier must use https.")
        self.issuer = issuer.rstrip("/")
        self.client_id = client_id
        self.resource = resource
        self.keys = key_source or jwt.PyJWKClient(self.issuer + "/.well-known/jwks.json", timeout=5)

    def verify(self, token: str) -> Principal:
        try:
            # Select a public key only from the trainer-configured pool. Never follow URLs inside the token.
            key = self.keys.get_signing_key_from_jwt(token).key
            claims = jwt.decode(token, key, algorithms=["RS256"], issuer=self.issuer,
                                audience=self.resource, options={"require": [
                                    "sub", "iss", "iat", "exp", "aud", "client_id", "token_use"]})
            if (not claims["sub"] or claims["token_use"] != "access"
                    or claims["client_id"] != self.client_id):
                raise InvalidCredential()
            groups = claims.get("cognito:groups", [])
            if not isinstance(groups, list) or not all(isinstance(g, str) for g in groups):
                raise InvalidCredential()
            policy = {"taskflow-reader": "reader", "taskflow-dispatcher": "dispatcher"}
            return Principal(claims["sub"], frozenset(policy[g] for g in groups if g in policy))
        except (jwt.PyJWTError, TypeError, ValueError, OverflowError) as exc:
            raise InvalidCredential("Cannot verify the access token") from exc


def create_cloud():
    # Friday targets a standard regional user pool issuer supplied by the trainer.
    issuer = os.environ["TF_COGNITO_ISSUER"].rstrip("/")
    parts = urlsplit(issuer)
    if (parts.scheme != "https" or not parts.hostname or not parts.hostname.startswith("cognito-idp.")
            or not parts.hostname.endswith(".amazonaws.com") or parts.netloc != parts.hostname
            or len(parts.path.strip("/").split("/")) != 1 or not parts.path.strip("/")
            or parts.query or parts.fragment):
        raise ValueError("Use the standard regional HTTPS pool issuer from your pool's discovery metadata.")
    return create_secure(provider=CognitoIdentity(issuer, os.environ["TF_COGNITO_CLIENT"],
                                                   os.environ["TF_COGNITO_RESOURCE"]))
