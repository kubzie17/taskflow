"""Runtime adapter for the protected Day 5 factory. Values arrive at startup."""
import os
from pathlib import Path

from exercises.day05_api import create_secure
from exercises.day05_identity import LocalIdentity


def application():
    required = ("TASKFLOW_DB", "TASKFLOW_IDENTITY_FILE", "APP_ENVIRONMENT")
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise RuntimeError("Missing runtime configuration: " + ", ".join(missing))
    database = Path(os.environ["TASKFLOW_DB"])
    # TODO A: read TASKFLOW_IDENTITY_FILE from the environment and wrap it in Path.
    identity = Path(os.environ["TASKFLOW_IDENTITY_FILE"])
    if not database.is_absolute() or not identity.is_absolute():
        raise RuntimeError("Runtime file paths must be absolute")
    if os.environ["APP_ENVIRONMENT"] not in {"training", "ci", "local"}:
        raise RuntimeError("APP_ENVIRONMENT must be training, ci or local")
    if not database.parent.is_dir():
        raise RuntimeError("The application data directory must already exist")
    try:
        provider = LocalIdentity.from_file(identity)
    except (OSError, ValueError, KeyError, TypeError, RuntimeError):
        raise RuntimeError("Runtime identity file is unavailable or invalid") from None
    return create_secure(db_path=database, provider=provider)
