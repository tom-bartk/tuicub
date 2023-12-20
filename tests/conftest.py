import asyncio
from datetime import datetime
from unittest.mock import Mock, create_autospec
from uuid import uuid4

import pytest
from asockit import SocketWriter
from eventoolkit import EventPublisher, EventsObserver
from httperactor import HttpClientBase
from httpx import Request
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyPressEvent
from prompt_toolkit.layout import Window
from prompt_toolkit.output import Output
from pydepot import Store

from src.tuicub.app.state import AppState
from src.tuicub.common.cache import Cache
from src.tuicub.common.config import Config
from src.tuicub.common.confirmation import ConfirmationService
from src.tuicub.common.confirmation.module import ConfirmationModule
from src.tuicub.common.events.module import EventsModule
from src.tuicub.common.http import BearerTokenAuthMiddleware
from src.tuicub.common.http.module import HttpModule
from src.tuicub.common.logger import Logger
from src.tuicub.common.models import (
    Game,
    Gameroom,
    GameroomStatus,
    GameState,
    Player,
    User,
)
from src.tuicub.common.module import CommonModule
from src.tuicub.common.screens import TuicubScreen
from src.tuicub.common.services.alert_service import AlertService
from src.tuicub.common.services.auth_service import AuthService
from src.tuicub.common.services.module import ServicesModule
from src.tuicub.common.state import State
from src.tuicub.common.state.module import StateModule
from src.tuicub.common.views import Theme


@pytest.fixture()
def config() -> Config:
    config = create_autospec(Config)
    config.api_url = "http://localhost:5000"
    return config


@pytest.fixture()
def initial_screen() -> TuicubScreen:
    screen = create_autospec(TuicubScreen)
    screen.__pt_container__ = Mock(return_value=Window())
    return screen


@pytest.fixture()
def common_module(config) -> CommonModule:
    common_module = create_autospec(CommonModule)
    common_module.config = config
    return common_module


@pytest.fixture()
def events_module() -> EventsModule:
    return create_autospec(EventsModule)


@pytest.fixture()
def output() -> Output:
    return create_autospec(Output)


@pytest.fixture()
def state_module() -> StateModule:
    return create_autospec(StateModule)


@pytest.fixture()
def http_module() -> HttpModule:
    return create_autospec(HttpModule)


@pytest.fixture()
def services_module() -> ServicesModule:
    return create_autospec(ServicesModule)


@pytest.fixture()
def confirmation_module() -> ConfirmationModule:
    return create_autospec(ConfirmationModule)


@pytest.fixture()
def theme() -> Theme:
    return create_autospec(Theme)


@pytest.fixture()
def loop() -> asyncio.AbstractEventLoop:
    return create_autospec(asyncio.AbstractEventLoop)


@pytest.fixture()
def events_publisher() -> EventPublisher:
    return create_autospec(EventPublisher)


@pytest.fixture()
def events_observer() -> EventsObserver:
    return create_autospec(EventsObserver)


@pytest.fixture()
def alert_service() -> AlertService:
    return create_autospec(AlertService)


@pytest.fixture()
def socket_writer() -> SocketWriter:
    return create_autospec(SocketWriter)


@pytest.fixture()
def store() -> Store[State]:
    return create_autospec(Store)


@pytest.fixture()
def cache() -> Cache:
    return create_autospec(Cache)


@pytest.fixture()
def app() -> Application:
    return create_autospec(Application)


@pytest.fixture()
def get_app(app) -> Mock:
    return Mock(return_value=app)


@pytest.fixture()
def app_store() -> Store[AppState]:
    return create_autospec(Store)


@pytest.fixture()
def logger() -> Logger:
    return create_autospec(Logger)


@pytest.fixture()
def event() -> KeyPressEvent:
    return create_autospec(KeyPressEvent)


@pytest.fixture()
def user_id_1() -> str:
    return str(uuid4())


@pytest.fixture()
def user_1(user_id_1) -> User:
    return User(id=user_id_1, name="Alice")


@pytest.fixture()
def user(user_1) -> User:
    return user_1


@pytest.fixture()
def user_id_2() -> str:
    return str(uuid4())


@pytest.fixture()
def user_2(user_id_2) -> User:
    return User(id=user_id_2, name="Bob")


@pytest.fixture()
def user_id_3() -> str:
    return str(uuid4())


@pytest.fixture()
def user_3(user_id_3) -> User:
    return User(id=user_id_3, name="Charlie")


@pytest.fixture()
def gameroom_id_1() -> str:
    return str(uuid4())


@pytest.fixture()
def gameroom_1(gameroom_id_1, user_id_1, user_1, user_2, user_3) -> Gameroom:
    return Gameroom(
        id=gameroom_id_1,
        created_at=datetime.now(),
        name="foo gameroom",
        owner_id=user_id_1,
        users=(user_1, user_2, user_3),
        game_id=None,
        status=GameroomStatus.STARTING,
    )


@pytest.fixture()
def gameroom(gameroom_1) -> Gameroom:
    return gameroom_1


@pytest.fixture()
def gameroom_id_2() -> str:
    return str(uuid4())


@pytest.fixture()
def gameroom_2(gameroom_id_2, user_id_2, user_1, user_2, game_id) -> Gameroom:
    return Gameroom(
        id=gameroom_id_2,
        created_at=datetime.now(),
        name="bar gameroom",
        owner_id=user_id_2,
        users=(user_1, user_2),
        game_id=game_id,
        status=GameroomStatus.RUNNING,
    )


@pytest.fixture()
def gameroom_id_3() -> str:
    return str(uuid4())


@pytest.fixture()
def gameroom_3(gameroom_id_3, user_id_3, user_3) -> Gameroom:
    return Gameroom(
        id=gameroom_id_3,
        created_at=datetime.now(),
        name="baz gameroom",
        owner_id=user_id_3,
        users=(user_3,),
        game_id=None,
        status=GameroomStatus.STARTING,
    )


@pytest.fixture()
def game_id() -> str:
    return str(uuid4())


@pytest.fixture()
def game(game_id, gameroom_id_1, user_id_1) -> Game:
    return Game(
        id=game_id,
        game_state=GameState(
            players=[
                Player(user_id=user_id_1, name="Alice", tiles_count=0, has_turn=False)
            ],
            board=[],
            pile_count=0,
            rack=[],
        ),
        gameroom_id=gameroom_id_1,
        winner=None,
    )


@pytest.fixture()
def auth_service() -> AuthService:
    return create_autospec(AuthService)


@pytest.fixture()
def auth_middleware() -> BearerTokenAuthMiddleware:
    return create_autospec(BearerTokenAuthMiddleware)


@pytest.fixture()
def confirmation_service() -> ConfirmationService:
    return create_autospec(ConfirmationService)


@pytest.fixture()
def http_client() -> HttpClientBase[Request]:
    return create_autospec(HttpClientBase)
