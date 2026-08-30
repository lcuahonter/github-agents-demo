# Changelog
<!-- Generado y mantenido automáticamente por el Documentation Agent -->
<!-- Formato: https://keepachangelog.com/es -->

## [2026-08-30] — commit `028ed9f`
### Actualizado
- feat: descripción    Closes #25

_Generado por Documentation Agent · autor: Luz Cuahonte_

---

## [2026-08-30] — commit `01a7413`
### Actualizado
- feat: descripción    Closes #23

_Generado por Documentation Agent · autor: Luz Cuahonte_

---

## [2026-08-30] — commit `6bfbfb2`
### Actualizado
- feat: descripción    Closes #21

_Generado por Documentation Agent · autor: Luz Cuahonte_

---

## [2026-08-28] — commit `fb88492`
### Actualizado
- feat: descripción    Closes #19

_Generado por Documentation Agent · autor: Luz Cuahonte_

---

## [2026-08-27] — commit `f91082e`
### Actualizado
- feat: descripción    Closes #17

_Generado por Documentation Agent · autor: Luz Cuahonte_

---

## [2026-08-26] — commit `6ecc290`
### Actualizado
- feat: descripción    Closes #15

_Generado por Documentation Agent · autor: Luz Cuahonte_

---

## [2026-08-26] — commit `51c1dc0`
### Actualizado
- feat: descripción

_Generado por Documentation Agent · autor: Luz Cuahonte_

---

## [2026-08-26] — commit `3448c16`
### Actualizado
- feat: descripción

_Generado por Documentation Agent · autor: Luz Cuahonte_

---

## [2026-08-26] — commit `7ef8ee7`
### Actualizado
- feat: descripción

_Generado por Documentation Agent · autor: Luz Cuahonte_

---

## [2026-08-26] — commit `af3ecc0`
### Actualizado
- feat: descripción

_Generado por Documentation Agent · autor: Luz Cuahonte_

---

## [2026-08-26] — commit `b059c24`
### Actualizado
- feat: descripción

_Generado por Documentation Agent · autor: Luz Cuahonte_

---

## [2026-08-26] — commit `a782d84`
### Actualizado
- feat: descripción

_Generado por Documentation Agent · autor: Luz Cuahonte_

---

## [2026-08-26] — commit `367eb7a`
### Actualizado
- feat: agregar función get_version al API

_Generado por Documentation Agent · autor: Luz Cuahonte_

---

## [2.1.0] - 2026-08-26
### Agregado
- `health_check()` — nuevo endpoint para monitoreo de salud de la API
- Soporte para moneda `MXN` en `process_payment()`

### Actualizado
- `OAuthHandler`: expiración de tokens reducida de 24h a 1h por mejora de seguridad
- `docs/api-reference.md`: documentación de `health_check()` y moneda MXN

_Generado por Documentation Agent · commit `abc1234` · autor: demo-user_

---

## [2.0.0] - 2026-07-15
### Agregado
- Módulo `src/auth/oauth_handler.py` con soporte para Google y GitHub
- Caché en memoria para tokens OAuth con TTL configurable
- Método `revoke_token()` para invalidación manual

### Modificado
- `process_payment()` ahora requiere autenticación vía `OAuthHandler`
- **Breaking change:** eliminado parámetro `api_key` del constructor anterior

### Seguridad
- Tokens ya no se loguean en texto plano; se truncan a 8 caracteres en las respuestas

_Generado por Documentation Agent · commit `def5678` · autor: demo-user_

---

## [1.0.0] - 2026-06-01
### Agregado
- Primera versión de `process_payment()` con validación básica de monto y moneda
- Soporte para `USD` y `EUR`

_Versión inicial del proyecto_
