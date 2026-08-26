"""
check_docs_coverage.py
Compara archivos .py en src/ contra entradas en docs/api-reference.md.
Exporta coverage_pct y missing_files al GITHUB_OUTPUT.
"""
import os
from pathlib import Path


THRESHOLD = 70  # % mínimo de cobertura antes de abrir un issue


def main():
    py_files = list(Path("src").rglob("*.py")) if Path("src").exists() else []
    py_files = [f for f in py_files if not f.name.startswith("_")]

    api_ref = Path("docs/api-reference.md")
    documented = set()

    if api_ref.exists():
        content = api_ref.read_text(encoding="utf-8")
        for f in py_files:
            if f.as_posix() in content or f.name in content:
                documented.add(f)

    total = len(py_files)
    covered = len(documented)
    pct = int((covered / total * 100)) if total > 0 else 100
    missing = [f.as_posix() for f in py_files if f not in documented]
    below = pct < THRESHOLD

    missing_md = "\n".join(f"- `{f}`" for f in missing) or "_Ninguno_"

    print(f"Cobertura documental: {pct}% ({covered}/{total})")
    print(f"Archivos sin documentar: {missing_md}")

    env_file = os.getenv("GITHUB_OUTPUT")
    if env_file:
        with open(env_file, "a") as fh:
            fh.write(f"coverage_pct={pct}\n")
            fh.write(f"coverage_below_threshold={'true' if below else 'false'}\n")
            fh.write(f"missing_files={missing_md}\n")


if __name__ == "__main__":
    main()
