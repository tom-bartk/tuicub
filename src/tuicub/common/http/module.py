import httpx
from httperactor import HttpClient, HttpClientBase

from ..module import CommonModule
from ..services.module import ServicesModule
from .auth_middleware import BearerTokenAuthMiddleware
from .client import TuicubHttpxClient
from .error_handler import AlertErrorHandler


class HttpModule:
    __slots__ = ("_auth_middleware", "_client")

    @property
    def auth_middleware(self) -> BearerTokenAuthMiddleware:
        return self._auth_middleware

    @property
    def client(self) -> HttpClientBase[httpx.Request]:
        return self._client

    def __init__(self, common_module: CommonModule, services_module: ServicesModule):
        self._auth_middleware: BearerTokenAuthMiddleware = BearerTokenAuthMiddleware(
            auth_service=services_module.auth_service
        )
        self._client: HttpClientBase[httpx.Request] = HttpClient(
            httpx_client=TuicubHttpxClient(
                config=common_module.config, logger=common_module.logger
            ),
            error_handler=AlertErrorHandler(alert_service=services_module.alert_service),
        )
