"""Optional browser sign-in. Send only an access token to the fixed loopback API; print statuses."""
import base64
import hashlib
import json
import os
import secrets
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import Request, urlopen

CALLBACK = "http://localhost:8765/callback"
API = "http://127.0.0.1:8055/tasks"


def run():
    domain = os.environ["TF_COGNITO_DOMAIN"].rstrip("/")
    host = urlsplit(domain)
    if (host.scheme != "https" or not host.hostname or not host.hostname.endswith(".amazoncognito.com")
            or host.netloc != host.hostname or host.path or host.query or host.fragment):
        raise SystemExit("Supply the standard HTTPS Cognito prefix domain you configured.")
    client = os.environ["TF_COGNITO_CLIENT"]
    resource = os.environ["TF_COGNITO_RESOURCE"]
    verifier = secrets.token_urlsafe(48)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("ascii")).digest()).rstrip(b"=").decode()
    state = secrets.token_urlsafe(24)
    result = {}

    class Callback(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass  # The redirect query contains the authorisation code.

        def do_GET(self):
            location = urlsplit(self.path)
            query = parse_qs(location.query)
            if location.path != "/callback" or query.get("state") != [state]:
                self.send_error(400, "Unexpected callback")
                return
            result["code"] = query.get("code", [""])[0]
            self.send_response(200)
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(b"Return to your terminal. You can close this tab.")

    params = {"response_type": "code", "client_id": client, "redirect_uri": CALLBACK,
              "scope": "openid", "resource": resource, "state": state,
              "code_challenge_method": "S256", "code_challenge": challenge, "prompt": "login"}
    with HTTPServer(("127.0.0.1", 8765), Callback) as server:
        server.timeout = 1
        webbrowser.open(domain + "/oauth2/authorize?" + urlencode(params))
        print("Complete the fictional sign-in in your browser (four-minute limit).")
        deadline = time.monotonic() + 240
        while not result and time.monotonic() < deadline:
            server.handle_request()
    if not result.get("code"):
        raise SystemExit("No confirmed authorisation code. Check callback, resource and app client.")
    body = urlencode({"grant_type": "authorization_code", "client_id": client,
                      "code": result["code"], "redirect_uri": CALLBACK, "code_verifier": verifier}).encode()
    try:
        with urlopen(Request(domain + "/oauth2/token", data=body), timeout=8) as r:
            access = json.load(r)["access_token"]
    except HTTPError as error:
        raise SystemExit(f"Token exchange returned HTTP {error.code}. No token displayed.")
    for method in ("GET", "POST"):
        payload = b'{"title":"Fictional Cognito booking"}' if method == "POST" else None
        request = Request(API, method=method, data=payload,
                          headers={"Authorization": "Bearer " + access, "Content-Type": "application/json"})
        try:
            with urlopen(request, timeout=5) as r:
                print(method, "/tasks", r.status)
        except HTTPError as error:
            print(method, "/tasks", error.code)


if __name__ == "__main__":
    run()
