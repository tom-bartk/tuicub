import pytest
from httperactor import HttpClient

from src.tuicub.common.http.auth_middleware import BearerTokenAuthMiddleware
from src.tuicub.common.http.module import HttpModule


@pytest.fixture()
def sut(common_module, services_module) -> HttpModule:
    return HttpModule(common_module=common_module, services_module=services_module)


class TestHttpModule:
    def test_auth_middleware__returns_bearer_token_auth_middleware_instance(
        self, sut
    ) -> None:
        result = sut.auth_middleware

        assert isinstance(result, BearerTokenAuthMiddleware)

    def test_client__returns_http_client_instance(self, sut) -> None:
        result = sut.client

        assert isinstance(result, HttpClient)
