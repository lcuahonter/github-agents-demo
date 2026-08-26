"""
generate_pr_description.py
Lee pr_diff.txt y genera una descripción en lenguaje natural más un checklist de docs.
Escribe los resultados en generated_pr_body.md y generated_docs_checklist.md.
"""
import os
import re
from pathlib import Path


def parse_changed_files(diff: str) -> list[str]:
    return re.findall(r"^diff --git a/(.+?) b/", diff, re.MULTILINE)


def classify_change(files: list[str]) -> tuple[str, list[str]]:
    """Return (change_type, docs_to_update)."""
    src_files = [f for f in files if f.startswith("src/")]
    doc_files = [f for f in files if f.startswith("docs/")]

    if any("auth" in f for f in src_files):
        change_type = "Cambio en módulo de autenticación"
    elif any("app" in f for f in src_files):
        change_type = "Cambio en API principal"
    else:
        change_type = "Cambio en código fuente"

    docs_needed = []
    if src_files:
        docs_needed.append("docs/api-reference.md")
        docs_needed.append("docs/CHANGELOG.md")
    if any("arch" in f or "config" in f for f in src_files):
        docs_needed.append("docs/architecture.md")

    return change_type, docs_needed


def main():
    diff_path = Path("pr_diff.txt")
    diff = diff_path.read_text(encoding="utf-8") if diff_path.exists() else ""

    title  = os.getenv("PR_TITLE", "Sin título")
    author = os.getenv("PR_AUTHOR", "unknown")
    base   = os.getenv("BASE_BRANCH", "main")

    changed = parse_changed_files(diff)
    change_type, docs_needed = classify_change(changed)

    # ── PR body ───────────────────────────────────────────────────────────────
    files_list = "\n".join(f"- `{f}`" for f in changed) or "- _(sin archivos detectados)_"
    docs_list  = "\n".join(f"- `{f}`" for f in docs_needed) or "- _(ninguna)_"

    pr_body = f"""\
## Descripción

**{change_type}** en la rama `{base}` por @{author}.

Este PR contiene los siguientes cambios:
{files_list}

### Impacto
Los cambios modifican la lógica de `{', '.join(changed[:2]) or 'archivos de código'}`.
Se recomienda revisar las pruebas existentes y la documentación relacionada.

### Documentación que debe actualizarse
{docs_list}

---
_Descripción generada automáticamente por el PR Description Agent 🤖_
"""

    # ── Docs checklist ────────────────────────────────────────────────────────
    checklist_items = "\n".join(
        f"- [ ] `{d}` — debe reflejar los cambios de este PR" for d in docs_needed
    ) or "- [ ] Sin documentación afectada detectada"

    checklist = f"""\
## 🤖 Revisión documental del agente

### Archivos modificados
{files_list}

### Documentación afectada
{checklist_items}
- [ ] `docs/CHANGELOG.md` — siempre debe incluir este cambio

### Checklist de calidad
- [ ] El código nuevo tiene docstrings suficientes
- [ ] Los parámetros nuevos están documentados
- [ ] El CHANGELOG refleja este cambio

---
_Generado por el Documentation Agent · No es necesario responder este comentario_
"""

    Path("generated_pr_body.md").write_text(pr_body, encoding="utf-8")
    Path("generated_docs_checklist.md").write_text(checklist, encoding="utf-8")
    print("✅ PR body y checklist generados")


if __name__ == "__main__":
    main()
