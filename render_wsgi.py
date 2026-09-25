"""Owner-only entry point for a temporary Render deployment.

Set ADAM_OWNER_PASSWORD as a secret in Render. Never commit its value.
"""

import base64
import binascii
import hmac
import os

from app import app as flask_app


class OwnerGate:
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __call__(self, environ, start_response):
        password = os.environ.get("ADAM_OWNER_PASSWORD", "")
        username = os.environ.get("ADAM_OWNER_USER", "adam")
        if len(password) < 10:
            return self._reply(start_response, "503 Service Unavailable", b"Owner password is not configured.\n")

        header = environ.get("HTTP_AUTHORIZATION", "")
        supplied_user = supplied_password = ""
        if header.startswith("Basic "):
            try:
                decoded = base64.b64decode(header[6:], validate=True).decode("utf-8")
                supplied_user, supplied_password = decoded.split(":", 1)
            except (ValueError, UnicodeDecodeError, binascii.Error):
                pass
        valid = hmac.compare_digest(supplied_user, username) & hmac.compare_digest(supplied_password, password)
        if not valid:
            return self._reply(start_response, "401 Unauthorized", b"Adam owner sign-in required.\n", challenge=True)
        return self.wrapped(environ, start_response)

    @staticmethod
    def _reply(start_response, status, body, challenge=False):
        headers = [("Content-Type", "text/plain; charset=utf-8"),
                   ("Content-Length", str(len(body))),
                   ("Cache-Control", "no-store"),
                   ("X-Content-Type-Options", "nosniff")]
        if challenge:
            headers.append(("WWW-Authenticate", 'Basic realm="Adam owner", charset="UTF-8"'))
        start_response(status, headers)
        return [body]


app = OwnerGate(flask_app)
