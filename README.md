# partner-docs-demo

![Docs Agent](https://github.com/actions/workflow/status/org/partner-docs-demo/docs-agent.yml/main?label=docs-agent&style=flat-square)
![PR Description](https://github.com/actions/workflow/status/org/partner-docs-demo/pr-description.yml/main?label=pr-description&style=flat-square)

> **Repositorio demo** para la presentación _"Repos, Projects, Actions y Pull Requests gestionados por agentes"_.
> Todo el contenido de `docs/` es generado y mantenido automáticamente por GitHub Copilot + Actions.

## ¿Qué hace este repo?

| Evento | Agente activado | Resultado |
|--------|----------------|-----------|
| Push a `main` con cambios en `src/` | `docs-agent.yml` | PR con docs actualizadas |
| Issue con label `needs-docs` | Copilot responde | Borrador de documentación como comentario |
| Pull Request abierto | `pr-description.yml` | Descripción + checklist auto-generados |
| Merge a `main` | `project-updater.yml` | Projects board actualizado |

## Estructura

```
partner-docs-demo/
├── .github/
│   ├── copilot-instructions.md    # Instrucciones del agente
│   ├── workflows/
│   │   ├── docs-agent.yml         # Genera docs en cada push
│   │   ├── pr-description.yml     # Describe PRs automáticamente
│   │   └── project-updater.yml    # Sincroniza Projects board
│   ├── ISSUE_TEMPLATE/
│   │   ├── feature_request.yml
│   │   ├── bug_report.yml
│   │   └── missing_docs.yml
│   └── PULL_REQUEST_TEMPLATE.md
├── src/
│   ├── app.py                     # API principal
│   └── auth/
│       └── oauth_handler.py       # Módulo de autenticación
├── docs/
│   ├── api-reference.md           # ← Generado por el agente
│   ├── architecture.md            # ← Generado por el agente
│   └── CHANGELOG.md               # ← Generado por el agente
└── README.md
```

## Cómo usar este template

```bash
# 1. Forkear o usar como template
gh repo create mi-proyecto --template org/partner-docs-demo

# 2. Activar GitHub Actions (ya viene configurado)
# 3. Adaptar .github/copilot-instructions.md a tu proyecto
# 4. Hacer un push y ver la magia
git push origin main
```

---

*Documentación mantenida automáticamente por GitHub Copilot Agent · Última actualización: automática en cada push*
