"""Heuristic content check; review all changes manually before publication."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "__pycache__", ".pytest_cache", ".venv", "build", "dist"}
PATTERNS = {
    "broker identifier": r"\bU\d{6,12}\b",
    "bot credential": r"\b\d{7,12}:[A-Za-z0-9_-]{30,}\b",
    "access credential": r"gh[pousr]_[A-Za-z0-9]{20,}",
    "private key": r"-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----",
    "personal email": r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b",
    "private path": r"(?i)(?:[A-Z]:[\\/](?:Users|QuantCore)|/" + r"Users/|/" + r"home/)",
}
FORBIDDEN = {"accounts.json", "config.json", ".env"}

def main():
    failures = []
    files = {p for p in ROOT.rglob("*") if p.is_file()
             and not (set(p.relative_to(ROOT).parts) & SKIP)
             and not any(part.endswith(".egg-info") for part in p.parts)}
    # Include tracked ignored files: ignore rules are not a security boundary.
    tracked = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True)
    if tracked.returncode == 0:
        files.update(ROOT / p for p in tracked.stdout.decode().split("\0") if p)
    for path in sorted(files):
        rel = path.relative_to(ROOT)
        if path.name in FORBIDDEN:
            failures.append(f"{rel}: forbidden configuration filename")
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError):
            failures.append(f"{rel}: unreadable or binary file requires review")
            continue
        for name, pattern in PATTERNS.items():
            if re.search(pattern, text):
                failures.append(f"{rel}: {name}")
    if failures:
        print("\n".join(failures))
        raise SystemExit(1)
    print(f"Public heuristic scan passed: {len(files)} text files; manual review still required.")

if __name__ == "__main__":
    main()
