import pytest

from src.tuicub.common.services.auth_service import AuthService


@pytest.fixture()
def sut() -> AuthService:
    return AuthService()


class TestSaveToken:
    def test_when_token_saved__get_token_returns_saved_token(self, sut) -> None:
        expected = "foo"

        sut.save_token(expected)
        result = sut.get_token()

        assert result == expected
