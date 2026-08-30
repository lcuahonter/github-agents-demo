# API Reference
<!-- Generado automáticamente por el Documentation Agent · No editar manualmente -->
<!-- Última actualización: 2026-08-30 · Commit: 01a7413 -->

## Visión general

Módulos actualizados en este commit:

- `src/app.py`
- `src/auth/oauth_handler.py`

---

## `src/app.py`

API principal - partner-docs-demo
Punto de entrada de la aplicación de pagos.

### `process_payment(amount, currency, user_id)` → `dict`

Procesa un pago verificando autenticación y validando montos.

### `health_check()` → `dict`

Retorna el estado de salud de la API.

### `get_version()` → `str`

Retorna la versión de la API.

### `list_currencies()` → `list`

Retorna las monedas soportadas por la API. 

### `list_paises()` → `list`

Retorna los paises soportados por la API. 

### `list_paises_bajo()` → `list`

Retorna los paises de bajo riesgo soportados por la API. 

### `list_paises_europa()` → `list`

Retorna los paises de Europa soportados por la API. 

### `list_paises_america()` → `list`

Retorna los paises de América soportados por la API. 

---

## `src/auth/oauth_handler.py`

Módulo de autenticación OAuth 2.0
Maneja tokens de acceso para los proveedores Google y GitHub.

### Clase `OAuthHandler`

Gestiona el ciclo de vida de tokens OAuth para usuarios autenticados.

### `__init__(provider)`

_Sin documentación._

### `get_token(user_id)` → `str`

Retorna un token válido para el usuario.
Si existe un token en caché y no ha expirado, lo reutiliza.

### `revoke_token(user_id)` → `bool`

Revoca el token activo de un usuario. Retorna True si existía.

### `health_check2()` → `dict`

Retorna el estado de salud de la API.

---


---
_Generado por el Documentation Agent · [Ver historial de cambios](CHANGELOG.md)_
