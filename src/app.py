"""
API principal - partner-docs-demo
Punto de entrada de la aplicación de pagos.
"""
from auth.oauth_handler import OAuthHandler


def process_payment(amount: float, currency: str, user_id: str) -> dict:
    """Procesa un pago verificando autenticación y validando montos."""
    if amount <= 0:
        raise ValueError("El monto debe ser mayor a cero")
    if currency not in ("USD", "EUR", "MXN"):
        raise ValueError(f"Moneda no soportada: {currency}")

    auth = OAuthHandler()
    token = auth.get_token(user_id)

    return {
        "status": "approved",
        "transaction_id": f"txn_{user_id}_{int(amount * 100)}",
        "amount": amount,
        "currency": currency,
        "token": token[:8] + "...",
    }


def health_check() -> dict:
    """Retorna el estado de salud de la API."""
    return {"status": "ok", "version": "2.1.2"}

def get_version() -> str:
    """Retorna la versión de la API."""
    return '2.1.4'

def list_currencies() -> list:
    """Retorna las monedas soportadas por la API. """
    return ["USD", "EUR", "MXN"]

def list_paises() -> list:
    """Retorna los paises soportados por la API. """
    return ["MX", "US", "ES"]
def list_paises_bajo() -> list:
    """Retorna los paises de bajo riesgo soportados por la API. """
    return ["MX", "US", "ES"]