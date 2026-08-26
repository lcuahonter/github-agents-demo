"""
Módulo de autenticación OAuth 2.0
Maneja tokens de acceso para los proveedores Google y GitHub.
"""
import hashlib
import time


class OAuthHandler:
    """Gestiona el ciclo de vida de tokens OAuth para usuarios autenticados."""

    SUPPORTED_PROVIDERS = ("google", "github")
    TOKEN_EXPIRY_SECONDS = 3600

    def __init__(self, provider: str = "github"):
        if provider not in self.SUPPORTED_PROVIDERS:
            raise ValueError(f"Proveedor no soportado: {provider}")
        self.provider = provider
        self._token_cache: dict[str, tuple[str, float]] = {}

    def get_token(self, user_id: str) -> str:
        """
        Retorna un token válido para el usuario.
        Si existe un token en caché y no ha expirado, lo reutiliza.
        """
        cached = self._token_cache.get(user_id)
        if cached:
            token, issued_at = cached
            if time.time() - issued_at < self.TOKEN_EXPIRY_SECONDS:
                return token

        token = self._generate_token(user_id)
        self._token_cache[user_id] = (token, time.time())
        return token

    def revoke_token(self, user_id: str) -> bool:
        """Revoca el token activo de un usuario. Retorna True si existía."""
        if user_id in self._token_cache:
            del self._token_cache[user_id]
            return True
        return False

    def _generate_token(self, user_id: str) -> str:
        """Genera un token determinístico basado en user_id y timestamp."""
        raw = f"{self.provider}:{user_id}:{time.time()}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def health_check(self) -> dict:
        """Retorna el estado de salud de la API."""
        return {"status": "ok", "version": "2.1.4"}
        
