from __future__ import annotations

from collections.abc import Callable

from eventoolkit import EventsObserver
from pydepot import Store

from ..common.events.module import EventsModule
from ..common.http.module import HttpModule
from ..common.models import Game, User
from ..common.module import CommonModule
from ..common.services.module import ServicesModule
from ..common.state.module import StateModule
from ..common.state.store import TuicubStore
from ..common.views import FocusWindow
from .actions import (
    AddDrawnTileReducer,
    EndTurnReducer,
    ResetStateReducer,
    SetHighlightedTileReducer,
    SetHighlightedTilesetReducer,
    SetTilesetsSelectionReducer,
    SetTilesSelectionReducer,
    SetWinnerReducer,
    StartTurnReducer,
    ToggleTileSelectedReducer,
    UpdateBoardReducer,
    UpdatePileCountReducer,
    UpdatePlayersReducer,
    UpdateRackReducer,
)
from .controller import GameController
from .errors import NoCurrentGameError, NoCurrentUserError
from .events import (
    BoardChangedEventHandler,
    PileCountChangedEventHandler,
    PlayerLeftEventHandler,
    PlayersChangedEventHandler,
    PlayerWonEventHandler,
    RackChangedEventHandler,
    TileDrawnEventHandler,
    TurnEndedEventHandler,
    TurnStartedEventHandler,
)
from .interactors.actions import ActionsInteractor
from .interactors.scroll import ScrollInteractor
from .keybinds import GameKeybindsContainer
from .requests.draw import DrawRequestInteractor
from .requests.end_turn import EndTurnRequestInteractor
from .requests.move import MoveRequestInteractor
from .requests.redo import RedoRequestInteractor
from .requests.undo import UndoRequestInteractor
from .services.board_service import BoardService
from .services.scroll_service import ScrollService
from .state import GameScreenState
from .view import GameRootView, GameScreen, GameView, GameWidgetFactory
from .viewmodel import GameViewModel
from .widgets.renderer import Renderer


class GameModule:
    @classmethod
    def assemble(
        cls,
        state_module: StateModule,
        services_module: ServicesModule,
        common_module: CommonModule,
        http_module: HttpModule,
        events_module: EventsModule,
    ) -> Callable[[], GameScreen]:
        def factory() -> GameScreen:
            game: Game | None = state_module.store.state.current_game
            if not game:
                raise NoCurrentGameError()

            user: User | None = state_module.store.state.current_user
            if not user:
                raise NoCurrentUserError()

            local_store: Store[GameScreenState] = TuicubStore(
                initial_state=GameScreenState.from_game(user_id=user.id, game=game),
                logger=common_module.logger,
            )
            local_store.register(AddDrawnTileReducer())
            local_store.register(EndTurnReducer())
            local_store.register(ResetStateReducer())
            local_store.register(SetHighlightedTileReducer())
            local_store.register(SetHighlightedTilesetReducer())
            local_store.register(SetTilesetsSelectionReducer())
            local_store.register(SetTilesSelectionReducer())
            local_store.register(SetWinnerReducer())
            local_store.register(StartTurnReducer())
            local_store.register(ToggleTileSelectedReducer())
            local_store.register(UpdateBoardReducer())
            local_store.register(UpdatePileCountReducer())
            local_store.register(UpdatePlayersReducer())
            local_store.register(UpdateRackReducer())

            scroll_service = ScrollService(
                cache=common_module.cache(),
                screen_size_service=services_module.screen_size_service,
            )

            viewmodel = GameViewModel(
                store=local_store,
                board_service=BoardService(
                    cache=common_module.cache(),
                    screen_size_service=services_module.screen_size_service,
                ),
                events_observer=EventsObserver(
                    BoardChangedEventHandler(store=local_store),
                    PileCountChangedEventHandler(store=local_store),
                    PlayerLeftEventHandler(
                        store=local_store, alert_service=services_module.alert_service
                    ),
                    PlayersChangedEventHandler(store=local_store),
                    PlayerWonEventHandler(store=local_store),
                    RackChangedEventHandler(store=local_store),
                    TileDrawnEventHandler(store=local_store),
                    TurnEndedEventHandler(store=local_store),
                    TurnStartedEventHandler(store=local_store),
                    publisher=events_module.publisher,
                ),
                scroll_service=scroll_service,
                user_id=user.id,
            )

            scroll_interactor = ScrollInteractor(
                scroll_service=scroll_service, store=local_store
            )
            move_interactor = MoveRequestInteractor(
                local_store=local_store,
                auth=http_module.auth_middleware,
                confirmation_service=services_module.confirmation_service,
                http_client=http_module.client,
                store=state_module.store,
            )
            undo_interactor = UndoRequestInteractor(
                local_store=local_store,
                auth=http_module.auth_middleware,
                confirmation_service=services_module.confirmation_service,
                http_client=http_module.client,
                store=state_module.store,
            )
            redo_interactor = RedoRequestInteractor(
                local_store=local_store,
                auth=http_module.auth_middleware,
                confirmation_service=services_module.confirmation_service,
                http_client=http_module.client,
                store=state_module.store,
            )
            end_turn_interactor = EndTurnRequestInteractor(
                local_store=local_store,
                auth=http_module.auth_middleware,
                confirmation_service=services_module.confirmation_service,
                http_client=http_module.client,
                store=state_module.store,
            )
            draw_interactor = DrawRequestInteractor(
                local_store=local_store,
                auth=http_module.auth_middleware,
                confirmation_service=services_module.confirmation_service,
                http_client=http_module.client,
                store=state_module.store,
            )
            actions_interactor = ActionsInteractor(
                move_interactor=move_interactor,
                undo_interactor=undo_interactor,
                redo_interactor=redo_interactor,
                end_turn_interactor=end_turn_interactor,
                draw_interactor=draw_interactor,
            )

            keybinds_container = GameKeybindsContainer(
                controller=GameController(
                    actions_interactor=actions_interactor,
                    alert_service=services_module.alert_service,
                    local_store=local_store,
                    scroll_interactor=scroll_interactor,
                    store=state_module.store,
                ),
                store=state_module.store,
                local_store=local_store,
                app_store=state_module.app_store,
            )

            return GameScreen(
                view=GameView(
                    viewmodel=viewmodel,
                    game_root_view=GameRootView(
                        factory=GameWidgetFactory(
                            viewmodel=viewmodel, theme=common_module.theme
                        ),
                        focus_window=FocusWindow(),
                        renderer=Renderer(theme=common_module.theme),
                    ),
                    keybinds_container=keybinds_container,
                ),
                keybinds_container=keybinds_container,
            )

        return factory
