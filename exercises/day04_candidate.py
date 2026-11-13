"""Northbridge local pilot candidate. Start with the workshop's Uvicorn factory command."""

from pathlib import Path

from fastapi import FastAPI

from app.main import create_app


def support_snapshot() -> dict[str, str]:
    """Return the support team's diagnostic snapshot using fictional lab identifiers."""
    return {
        "status": "ok",
        "service": "taskflow",
        "support_node": "nb-lab-amber-02",
        "runbook": "NB-DEMO-17",
    }


def create_candidate(db_path: Path | None = None) -> FastAPI:
    """Extend the learner's existing TaskFlow app against a separate workshop database."""
    store = db_path if db_path is not None else Path("data/day04-lab.db")
    api = create_app(store)

    @api.get("/support/status")
    def support_status() -> dict[str, str]:
        snapshot = support_snapshot()
        return {"status": snapshot["status"], "service": snapshot["service"]}

    return api
