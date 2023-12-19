from unittest.mock import Mock, create_autospec

import httpx
import pytest

from src.tuicub.common.http import BearerTokenAuthMiddleware


@pytest.fixture()
def sut(auth_service) -> BearerTokenAuthMiddleware:
    return BearerTokenAuthMiddleware(auth_service=auth_service)


class TestApply:
    def test__adds_authorization_header_with_token_from_auth_service(
        self, sut: BearerTokenAuthMiddleware, auth_service
    ) -> None:
        auth_service.get_token = Mock(return_value="foo")
        request = create_autospec(httpx.Request)
        request.headers = {}

        result = sut.apply(request=request)

        assert result.headers["Authorization"] == "Bearer foo"
