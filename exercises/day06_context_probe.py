"""Optional Docker BuildKit proof using synthetic files in a new temporary directory."""
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    if not (ROOT / ".dockerignore").is_file():
        raise SystemExit("No root .dockerignore. Inspect the Day 3 build context before testing.")
    with tempfile.TemporaryDirectory(prefix="taskflow-d6-context-") as temporary:
        root = Path(temporary)
        context = root / "fixture"
        (context / "app").mkdir(parents=True)
        shutil.copyfile(ROOT / ".dockerignore", context / ".dockerignore")
        (context / "Dockerfile").write_text("FROM scratch\nCOPY . /proof/\n", encoding="utf-8")
        (context / "app/main.py").write_text("# harmless fixture\n", encoding="utf-8")
        (context / "app/dispatch.local.env").write_text("DUMMY=TRAINING_ONLY_NOT_A_CREDENTIAL\n", encoding="utf-8")
        output = root / "result"
        try:
            result = subprocess.run(["docker", "buildx", "build", "--output", "type=local,dest="+str(output),
                                     str(context)])
        except FileNotFoundError:
            raise SystemExit("Docker unavailable. Record the rule inspection and leave the build untested.")
        if result.returncode:
            raise SystemExit("The builder did not complete. Context exclusion is untested.")
        app_visible = (output / "proof/app/main.py").is_file()
        marker_visible = (output / "proof/app/dispatch.local.env").is_file()
        print("Application file included:", app_visible, "| fictional marker included:", marker_visible)
        return 0 if app_visible and not marker_visible else 1


if __name__ == "__main__":
    raise SystemExit(main())
