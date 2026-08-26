# API Reference
<!-- Generado automáticamente por el Documentation Agent · No editar manualmente -->
<!-- Última actualización: 2026-08-26 · Commit: abc1234 -->

## Visión general

`partner-docs-demo` expone dos módulos principales:

| Módulo | Archivo | Descripción |
|--------|---------|-------------|
| API principal | `src/app.py` | Procesamiento de pagos y health check |
| Autenticación OAuth | `src/auth/oauth_handler.py` | Gestión de tokens OAuth 2.0 |

---

## `src/app.py`

### `process_payment(amount, currency, user_id)`

Procesa un pago verificando autenticación del usuario y validando el monto y moneda.

**Parámetros**

| Nombre | Tipo | Requerido | Descripción |
|--------|------|-----------|-------------|
| `amount` | `float` | ✅ | Monto a cobrar. Debe ser mayor a `0`. |
| `currency` | `str` | ✅ | Código de moneda ISO 4217. Valores aceptados: `USD`, `EUR`, `MXN`. |
| `user_id` | `str` | ✅ | Identificador único del usuario autenticado. |

**Retorno** `dict`

```json
{
  "status": "approved",
  "transaction_id": "txn_user123_5000",
  "amount": 50.00,
  "currency": "USD",
  "token": "a3f8bc12..."
}
```

**Excepciones**

| Excepción | Motivo |
|-----------|--------|
| `ValueError` | `amount <= 0` o moneda no soportada |

**Ejemplo de uso**

```python
from src.app import process_payment

result = process_payment(
    amount=99.99,
    currency="USD",
    user_id="user_42"
)
print(result["transaction_id"])  # txn_user_42_9999
```

---

### `health_check()`

Retorna el estado de salud de la API. Útil para load balancers y monitoreo.

**Parámetros:** ninguno

**Retorno** `dict`

```json
{ "status": "ok", "version": "2.1.0" }
```

**Ejemplo de uso**

```python
from src.app import health_check

print(health_check())  # {'status': 'ok', 'version': '2.1.0'}
```

---

## `src/auth/oauth_handler.py`

### Clase `OAuthHandler`

Gestiona el ciclo de vida de tokens OAuth 2.0 para usuarios autenticados.
Implementa un caché en memoria con expiración automática de tokens.

**Proveedores soportados:** `"google"`, `"github"`

**Constructor**

```python
OAuthHandler(provider: str = "github")
```

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `provider` | `str` | `"github"` | Proveedor OAuth. Ver `SUPPORTED_PROVIDERS`. |

**Excepciones del constructor**

| Excepción | Motivo |
|-----------|--------|
| `ValueError` | Proveedor no incluido en `SUPPORTED_PROVIDERS` |

---

### `get_token(user_id)`

Retorna un token OAuth válido para el usuario. Reutiliza el caché si el token no ha expirado (1 hora).

**Parámetros**

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `user_id` | `str` | Identificador único del usuario |

**Retorno:** `str` — Token SHA-256 hexadecimal de 64 caracteres

**Ejemplo de uso**

```python
auth = OAuthHandler(provider="google")
token = auth.get_token("user_42")
print(token[:8])  # ej. "a3f8bc12"
```

---

### `revoke_token(user_id)`

Revoca (elimina del caché) el token activo de un usuario.

**Parámetros**

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `user_id` | `str` | Identificador del usuario cuyo token se revoca |

**Retorno:** `bool` — `True` si el token existía y fue eliminado, `False` si no había token activo

**Ejemplo de uso**

```python
auth = OAuthHandler()
auth.get_token("user_42")        # genera el token
auth.revoke_token("user_42")     # True — token eliminado
auth.revoke_token("user_99")     # False — no existía
```

---

## Notas de seguridad

- Los tokens se generan con SHA-256 sobre `provider:user_id:timestamp`. No son tokens JWT ni se validan contra un servidor externo en este demo.
- En producción, reemplazar `_generate_token` por la integración real con el proveedor OAuth.
- El caché es en memoria; se pierde al reiniciar el proceso. Usar Redis u otro store compartido en producción.

---

_Generado por el Documentation Agent · [Ver historial de cambios](CHANGELOG.md)_
