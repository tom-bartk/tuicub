from unittest.mock import Mock, create_autospec, patch

import pytest
from pydepot import Store

from src.tuicub.register_user.controller import RegisterUserController
from src.tuicub.register_user.request import RegisterUserInteractor
from src.tuicub.register_user.state import RegisterUserState, SetNameAction


@pytest.fixture()
def local_store() -> Store[RegisterUserState]:
    return create_autospec(Store)


@pytest.fixture()
def register_user_interactor() -> RegisterUserInteractor:
    interactor = Mock()
    interactor.register_user = Mock()
    return interactor


@pytest.fixture()
def sut(store, local_store, register_user_interactor) -> RegisterUserController:
    return RegisterUserController(
        store=store,
        local_store=local_store,
        register_user_interactor=register_user_interactor,
    )


class TestOnTextChanged:
    def test_dispatches_set_name_action_to_local_store_with_new_text(
        self, sut, local_store
    ) -> None:
        expected = SetNameAction(name="foo")

        sut.on_text_changed(text="foo")

        local_store.dispatch.assert_called_once_with(expected)


class TestRegisterUser:
    def test_executes_register_user_request(
        self, sut, event, register_user_interactor
    ) -> None:
        with patch("src.tuicub.common.utils.async_run") as mock_async_run:
            sut.register_user(event)

            mock_async_run.assert_called_once()
            register_user_interactor.execute.assert_called_once()
