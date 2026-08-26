"""
generate_docs.py
Lee los archivos Python modificados (CHANGED_FILES env var) y genera/actualiza
docs/api-reference.md extrayendo docstrings y firmas de funciones/clases.
"""
import ast
import os
import sys
from pathlib import Path


HEADER = """\
# API Reference
<!-- Generado automáticamente por el Documentation Agent · No editar manualmente -->
<!-- Última actualización: {date} · Commit: {sha} -->

"""

FOOTER = "\n---\n_Generado por el Documentation Agent · [Ver historial de cambios](CHANGELOG.md)_\n"


def extract_module_docs(path: Path) -> str:
    """Parse a Python file and return its Markdown documentation."""
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except SyntaxError as e:
        return f"> ⚠️ No se pudo analizar `{path}`: {e}\n"

    lines = []
    module_doc = ast.get_docstring(tree)
    rel = path.as_posix()

    lines.append(f"## `{rel}`\n")
    if module_doc:
        lines.append(f"{module_doc}\n")

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # skip private helpers
            if node.name.startswith("_") and not node.name.startswith("__"):
                continue
            doc = ast.get_docstring(node) or "_Sin documentación._"
            args = [a.arg for a in node.args.args if a.arg != "self"]
            ret = ""
            if node.returns:
                ret = f" → `{ast.unparse(node.returns)}`"
            lines.append(f"### `{node.name}({', '.join(args)})`{ret}\n")
            lines.append(f"{doc}\n")

        elif isinstance(node, ast.ClassDef):
            doc = ast.get_docstring(node) or "_Sin documentación._"
            lines.append(f"### Clase `{node.name}`\n")
            lines.append(f"{doc}\n")

    return "\n".join(lines)


def main():
    sha = os.getenv("GITHUB_SHA", "unknown")[:7]
    from datetime import date
    today = date.today().isoformat()

    # Always document all src/ Python files so coverage never drops
    src_root = Path("src")
    py_files = sorted(
        f for f in src_root.rglob("*.py")
        if f.exists() and not f.name.startswith("_")
    ) if src_root.exists() else []

    if not py_files:
        print("No hay archivos Python en src/. Nada que documentar.")
        sys.exit(0)

    docs_path = Path("docs/api-reference.md")
    docs_path.parent.mkdir(exist_ok=True)

    content = HEADER.format(date=today, sha=sha)
    content += "## Visión general\n\nMódulos actualizados en este commit:\n\n"
    content += "\n".join(f"- `{f}`" for f in py_files) + "\n\n---\n\n"

    for f in py_files:
        content += extract_module_docs(f) + "\n---\n\n"

    content += FOOTER
    docs_path.write_text(content, encoding="utf-8")
    print(f"✅ Documentación generada en {docs_path}")

    # Expose summary for the PR body
    summary = f"Se actualizaron: {', '.join(f'`{f}`' for f in py_files)}"
    env_file = os.getenv("GITHUB_OUTPUT")
    if env_file:
        with open(env_file, "a") as fh:
            fh.write(f"summary={summary}\n")


if __name__ == "__main__":
    main()
