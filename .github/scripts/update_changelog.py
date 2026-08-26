"""
update_changelog.py
Agrega una entrada al CHANGELOG.md basada en el commit actual.
"""
import os
from datetime import datetime
from pathlib import Path


CHANGELOG = Path("docs/CHANGELOG.md")


def main():
    sha     = os.getenv("COMMIT_SHA", "unknown")[:7]
    msg     = os.getenv("COMMIT_MSG", "sin mensaje")
    author  = os.getenv("COMMIT_AUTHOR", "unknown")
    raw_date = os.getenv("RUN_DATE", "")

    try:
        dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
        date_str = dt.strftime("%Y-%m-%d")
    except (ValueError, AttributeError):
        date_str = datetime.now().strftime("%Y-%m-%d")

    entry = (
        f"\n## [{date_str}] — commit `{sha}`\n"
        f"### Actualizado\n"
        f"- {msg}\n\n"
        f"_Generado por Documentation Agent · autor: {author}_\n\n---\n"
    )

    CHANGELOG.parent.mkdir(exist_ok=True)
    existing = CHANGELOG.read_text(encoding="utf-8") if CHANGELOG.exists() else "# Changelog\n"

    # Insert after the first heading
    if "\n## " in existing:
        insert_at = existing.index("\n## ")
        updated = existing[:insert_at] + entry + existing[insert_at:]
    else:
        updated = existing + entry

    CHANGELOG.write_text(updated, encoding="utf-8")
    print(f"✅ CHANGELOG actualizado con entrada para commit {sha}")


if __name__ == "__main__":
    main()
