import httpx
from httperactor import AuthMiddleware

from ..services.auth_service import AuthService


class BearerTokenAuthMiddleware(AuthMiddleware[httpx.Request]):
    """An auth middleware that appends a 'Bearer token' authorization header."""

    __slots__ = ("_auth_service",)

    def __init__(self, auth_service: AuthService):
        self._auth_service: AuthService = auth_service

    def apply(self, request: httpx.Request) -> httpx.Request:
        """Add authentication to a request.

        Appends the 'Authorization' header containing the 'Bearer token'.

        Args:
            request (httpx.Request): The request to authenticate.

        Returns:
            The authenticated request.
        """
        request.headers["Authorization"] = f"Bearer {self._auth_service.get_token()}"
        return request
