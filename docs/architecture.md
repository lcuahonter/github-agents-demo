# Arquitectura del sistema
<!-- Generado automáticamente por el Documentation Agent -->

## Visión general

`partner-docs-demo` es una aplicación de procesamiento de pagos con autenticación OAuth 2.0.
El sistema está diseñado para demostrar el flujo de documentación automática mediante GitHub Copilot Agents.

## Diagrama de componentes

```
┌─────────────────────────────────────────────────┐
│                  GitHub                          │
│                                                  │
│  ┌──────────┐   Push/PR/Issue                   │
│  │  Dev     │─────────────────────────────────┐  │
│  └──────────┘                                 │  │
│                                               ▼  │
│  ┌─────────────────────────────────────────────┐ │
│  │           GitHub Actions                    │ │
│  │                                             │ │
│  │  docs-agent.yml ──► Copilot API             │ │
│  │  pr-description.yml                         │ │
│  │  project-updater.yml                        │ │
│  └──────────────────────┬──────────────────────┘ │
│                         │                        │
│              ┌──────────┴──────────┐             │
│              ▼                     ▼             │
│         docs/ (PR)         Projects board        │
└─────────────────────────────────────────────────┘

Aplicación (src/)
├── app.py              # Capa de API — entry points
└── auth/
    └── oauth_handler.py # Capa de autenticación
```

## Flujo de datos · Procesamiento de pago

```
Cliente
  │
  ├─► process_payment(amount, currency, user_id)
  │         │
  │         ├─► Validación de parámetros
  │         │         └─► ValueError si inválidos
  │         │
  │         └─► OAuthHandler.get_token(user_id)
  │                   │
  │                   ├─► Cache hit? → retorna token existente
  │                   └─► Cache miss → _generate_token() → actualiza caché
  │
  └─◄ { status, transaction_id, amount, currency, token }
```

## Decisiones de diseño

| Decisión | Razón |
|----------|-------|
| Caché en memoria para tokens | Simplicidad para el demo. En producción usar Redis. |
| SHA-256 como token | Determinístico y reproducible para testing. No usar en producción real. |
| Monedas hard-coded | Scope limitado del demo. En producción usar tabla de configuración. |

## Dependencias

| Librería | Versión | Uso |
|----------|---------|-----|
| `openai` | 1.40.0 | Integración con Copilot API en los workflows |
| `gitpython` | 3.1.43 | Análisis de diffs en scripts de Actions |

---

_Generado por el Documentation Agent · [Ver API Reference](api-reference.md)_
