"""
respond_to_issue.py
Lee el body del issue, extrae la ruta del archivo mencionado,
y genera un borrador de documentación como comentario Markdown.
"""
import ast
import os
import re
from pathlib import Path


def find_file_in_text(text: str) -> Path | None:
    """Busca una ruta de archivo Python mencionada en el texto del issue."""
    match = re.search(r"(src/[\w/]+\.py)", text)
    if match:
        p = Path(match.group(1))
        return p if p.exists() else None
    # fallback: primer .py del repo
    candidates = list(Path("src").rglob("*.py")) if Path("src").exists() else []
    return candidates[0] if candidates else None


def generate_draft(path: Path) -> str:
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except (SyntaxError, OSError):
        return f"> ⚠️ No se pudo analizar `{path}`."

    sections = []
    module_doc = ast.get_docstring(tree) or "Sin descripción de módulo."
    sections.append(f"**Módulo:** `{path.as_posix()}`\n\n{module_doc}")

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("_"):
                continue
            args = [a.arg for a in node.args.args if a.arg != "self"]
            doc = ast.get_docstring(node) or "_Sin docstring — por favor agregar descripción._"

            # Build param table
            param_rows = "\n".join(
                f"| `{a}` | `any` | — |" for a in args
            ) or "| — | — | — |"

            ret = ""
            if node.returns:
                try:
                    ret = f"`{ast.unparse(node.returns)}`"
                except Exception:
                    ret = "`unknown`"
            else:
                ret = "`None`"

            sections.append(
                f"### `{node.name}({', '.join(args)})`\n\n"
                f"{doc}\n\n"
                f"**Parámetros**\n\n"
                f"| Nombre | Tipo | Descripción |\n"
                f"|--------|------|-------------|\n"
                f"{param_rows}\n\n"
                f"**Retorno:** {ret}\n\n"
                f"**Ejemplo de uso**\n\n"
                f"```python\n# TODO: agregar ejemplo para {node.name}\n```"
            )

        elif isinstance(node, ast.ClassDef):
            doc = ast.get_docstring(node) or "_Sin docstring de clase._"
            sections.append(f"### Clase `{node.name}`\n\n{doc}")

    return "\n\n---\n\n".join(sections)


def main():
    issue_body = os.getenv("ISSUE_BODY", "")
    author = os.getenv("ISSUE_AUTHOR", "unknown")

    target = find_file_in_text(issue_body)

    if not target:
        comment = (
            "## 📄 Agente de documentación\n\n"
            "> No encontré un archivo `.py` específico en tu issue. "
            "Por favor menciona la ruta exacta (ej. `src/auth/oauth_handler.py`) "
            "para que pueda generar el borrador.\n\n"
            f"@{author}"
        )
    else:
        draft = generate_draft(target)
        comment = (
            f"## 📄 Borrador de documentación generado por el agente\n\n"
            f"> Archivo analizado: `{target.as_posix()}`\n\n"
            f"{draft}\n\n"
            "---\n"
            f"_Generado automáticamente. Revisa, ajusta y aprueba antes de mergear._\n\n"
            f"@{author} — puedes editar directamente este borrador o hacer commit del archivo "
            f"`docs/api-reference.md` actualizado."
        )

    Path("issue_comment.md").write_text(comment, encoding="utf-8")
    print(f"✅ Comentario generado para archivo: {target}")


if __name__ == "__main__":
    main()
