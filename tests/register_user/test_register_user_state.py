import pytest

from src.tuicub.register_user.state import (
    RegisterUserState,
    SetNameAction,
    SetNameReducer,
)


@pytest.fixture()
def name() -> str:
    return "foo"


class TestSetNameReducer:
    @pytest.fixture()
    def sut(self) -> SetNameReducer:
        return SetNameReducer()

    def test_action_type__returns_set_name_action(self, sut: SetNameReducer) -> None:
        expected = SetNameAction

        result = sut.action_type

        assert result == expected

    def test_apply__returns_new_state_with_name_from_action(
        self, sut: SetNameReducer
    ) -> None:
        current = RegisterUserState(name="foo")
        expected = RegisterUserState(name="bar")

        result = sut.apply(action=SetNameAction(name="bar"), state=current)

        assert result == expected
