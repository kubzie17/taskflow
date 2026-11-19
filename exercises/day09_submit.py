"""Submit the fixed course SSM document and wait for its real command result."""
import json
import os
import re
import subprocess
import time


def aws(*args):
    return json.loads(subprocess.run(["aws", *args, "--region", os.environ["AWS_REGION"], "--output", "json"],
                                    check=True, text=True, capture_output=True).stdout)


def main():
    digest = os.environ["IMAGE_DIGEST"]
    instance = os.environ["INSTANCE_ID"]
    doc = os.environ["SSM_DOCUMENT"]
    port = os.environ["APP_PORT"]
    app_env = os.environ["APP_ENVIRONMENT"]
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
        raise ValueError("Invalid image digest")
    if not re.fullmatch(r"i-[0-9a-f]{8,17}", instance):
        raise ValueError("Invalid instance ID")
    if not re.fullmatch(r"TaskFlow-Day09-[a-z0-9-]+", doc):
        raise ValueError("Invalid document name")
    if port != "8055" or app_env != "training":
        raise ValueError("This course document expects port 8055 and environment training")
    result = aws("ssm", "send-command", "--instance-ids", instance, "--document-name", doc,
                 "--document-version", "1", "--timeout-seconds", "600", "--parameters",
                 json.dumps({"ImageDigest": [digest], "AppEnvironment": [app_env], "AppPort": [port]}))
    command = result["Command"]["CommandId"]
    print("SSM command", command)
    for _ in range(100):
        time.sleep(6)
        try:
            result = aws("ssm", "get-command-invocation", "--command-id", command, "--instance-id", instance)
        except subprocess.CalledProcessError as error:
            if "InvocationDoesNotExist" in (error.stderr or ""):
                continue
            raise
        if result["Status"] == "Success":
            print("Deployment command succeeded. Complete the authenticated learner probe through the SSM tunnel.")
            return
        if result["Status"] not in {"Pending", "InProgress", "Delayed"}:
            raise RuntimeError("SSM command ended with " + result["Status"] + ". Inspect its output in AWS.")
    raise RuntimeError("SSM wait timed out. Inspect the existing command before retrying.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.CalledProcessError) as error:
        print("Deployment has not passed verification.")
        if isinstance(error, (ValueError, RuntimeError)):
            print(str(error))
        raise SystemExit(1) from None
