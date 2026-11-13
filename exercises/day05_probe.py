"""Send a local negative test without displaying or signing tokens. Use only your own lab."""
import base64
import getpass
import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def segment(data):
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def private_sign_in():
    name = input("Fictional username: ").strip()
    password = getpass.getpass("Fictional passphrase: ")
    body = json.dumps({"username": name, "password": password}).encode()
    request = Request("http://127.0.0.1:8055/session", data=body, headers={"Content-Type": "application/json"})
    try:
        with urlopen(request, timeout=5) as response:
            print("POST /session", response.status)
            token = json.load(response)["access_token"]
    except HTTPError as error:
        print("POST /session", error.code)
        return
    title = input("Fictional title for a booking attempt: ").strip()
    for method in ("GET", "POST", "GET"):
        payload = json.dumps({"title": title}).encode() if method == "POST" else None
        resource = Request("http://127.0.0.1:8055/tasks", data=payload, method=method,
                           headers={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        try:
            with urlopen(resource, timeout=5) as response:
                print(method, "/tasks", response.status, json.load(response))
        except HTTPError as error:
            print(method, "/tasks", error.code)


def main():
    choice = input("Enter login, missing, malformed, tamper, as-is or spoof: ").strip().lower()
    if choice == "login":
        private_sign_in()
        return
    headers = {"Content-Type": "application/json"}
    if choice in {"tamper", "as-is"}:
        token = getpass.getpass("Paste your local access token privately: ").strip()
        if choice == "tamper":
            head, body, sig = token.split(".")
            claims = json.loads(base64.urlsafe_b64decode(body + "==="))
            claims["roles"] = ["dispatcher", "tampered"]
            token = ".".join((head, segment(json.dumps(claims).encode()), sig))
        headers["Authorization"] = "Bearer " + token
    elif choice == "malformed":
        headers["Authorization"] = "Bearer fictional.not-a-token"
    elif choice == "spoof":
        headers["X-Role"] = "dispatcher"
    elif choice != "missing":
        raise SystemExit("Unknown probe.")
    request = Request("http://127.0.0.1:8055/tasks", data=b'{"title":"Fictional gate probe"}', headers=headers)
    try:
        with urlopen(request, timeout=5) as response:
            print("POST /tasks", response.status)
    except HTTPError as error:
        print("POST /tasks", error.code)


if __name__ == "__main__":
    main()
