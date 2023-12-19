import pytest

from src.tuicub.common.views import ScrollDirection
from src.tuicub.gamerooms.state import (
    GameroomsState,
    ScrollGameroomsAction,
    ScrollGameroomsReducer,
    SetGameroomsRowsAction,
    SetGameroomsRowsReducer,
)
from src.tuicub.gamerooms.view import GameroomRowViewModel


class TestSetGameroomsRowsReducer:
    @pytest.fixture()
    def sut(self) -> SetGameroomsRowsReducer:
        return SetGameroomsRowsReducer()

    def test_action_type__returns_set_gamerooms_rows_action(
        self, sut: SetGameroomsRowsReducer
    ) -> None:
        expected = SetGameroomsRowsAction

        result = sut.action_type

        assert result == expected

    def test_apply__when_selected_index_lt_gamerooms_len__row_at_selected_index_is_highlighted(  # noqa: E501
        self, sut: SetGameroomsRowsReducer, gameroom_1, gameroom_2, gameroom_3
    ) -> None:
        current = GameroomsState(selected_index=1)
        expected = GameroomsState(
            rows=(
                GameroomRowViewModel(gameroom=gameroom_1, is_highlighted=False),
                GameroomRowViewModel(gameroom=gameroom_2, is_highlighted=True),
                GameroomRowViewModel(gameroom=gameroom_3, is_highlighted=False),
            ),
            selected_index=1,
        )

        result = sut.apply(
            action=SetGameroomsRowsAction(gamerooms=(gameroom_1, gameroom_2, gameroom_3)),
            state=current,
        )

        assert result == expected

    def test_apply__when_selected_index_gte_gamerooms_len__last_row_is_highlighted(
        self, sut: SetGameroomsRowsReducer, gameroom_1, gameroom_2, gameroom_3
    ) -> None:
        current = GameroomsState(selected_index=42)
        expected = GameroomsState(
            rows=(
                GameroomRowViewModel(gameroom=gameroom_1, is_highlighted=False),
                GameroomRowViewModel(gameroom=gameroom_2, is_highlighted=False),
                GameroomRowViewModel(gameroom=gameroom_3, is_highlighted=True),
            ),
            selected_index=2,
        )

        result = sut.apply(
            action=SetGameroomsRowsAction(gamerooms=(gameroom_1, gameroom_2, gameroom_3)),
            state=current,
        )

        assert result == expected

    def test_apply__when_selected_index_gt_0__gamerooms_empty__returned_selected_index_is_0(  # noqa: E501
        self, sut: SetGameroomsRowsReducer
    ) -> None:
        current = GameroomsState(selected_index=42)
        expected = GameroomsState(rows=(), selected_index=0)

        result = sut.apply(action=SetGameroomsRowsAction(gamerooms=()), state=current)

        assert result == expected


class TestScrollGameroomsReducer:
    @pytest.fixture()
    def sut(self) -> ScrollGameroomsReducer:
        return ScrollGameroomsReducer()

    def test_action_type__returns_set_gamerooms_rows_action(
        self, sut: ScrollGameroomsReducer
    ) -> None:
        expected = ScrollGameroomsAction

        result = sut.action_type

        assert result == expected

    def test_apply__when_up__selected_index_0__does_nothing(
        self, sut: ScrollGameroomsReducer, gameroom_1, gameroom_2, gameroom_3
    ) -> None:
        current = GameroomsState(
            rows=(
                GameroomRowViewModel(gameroom=gameroom_1, is_highlighted=True),
                GameroomRowViewModel(gameroom=gameroom_2, is_highlighted=False),
                GameroomRowViewModel(gameroom=gameroom_3, is_highlighted=False),
            ),
            selected_index=0,
        )

        result = sut.apply(
            action=ScrollGameroomsAction(direction=ScrollDirection.UP), state=current
        )

        assert result == current

    def test_apply__when_up__selected_index_gte_rows_count__does_nothing(
        self, sut: ScrollGameroomsReducer, gameroom_1, gameroom_2, gameroom_3
    ) -> None:
        current = GameroomsState(
            rows=(
                GameroomRowViewModel(gameroom=gameroom_1, is_highlighted=True),
                GameroomRowViewModel(gameroom=gameroom_2, is_highlighted=False),
                GameroomRowViewModel(gameroom=gameroom_3, is_highlighted=False),
            ),
            selected_index=42,
        )

        result = sut.apply(
            action=ScrollGameroomsAction(direction=ScrollDirection.UP), state=current
        )

        assert result == current

    def test_apply__when_up__selected_index_neq_0_and_lt_rows_count__scrolls_up(
        self, sut: ScrollGameroomsReducer, gameroom_1, gameroom_2, gameroom_3
    ) -> None:
        current = GameroomsState(
            rows=(
                GameroomRowViewModel(gameroom=gameroom_1, is_highlighted=False),
                GameroomRowViewModel(gameroom=gameroom_2, is_highlighted=True),
                GameroomRowViewModel(gameroom=gameroom_3, is_highlighted=False),
            ),
            selected_index=1,
        )
        expected = GameroomsState(
            rows=(
                GameroomRowViewModel(gameroom=gameroom_1, is_highlighted=True),
                GameroomRowViewModel(gameroom=gameroom_2, is_highlighted=False),
                GameroomRowViewModel(gameroom=gameroom_3, is_highlighted=False),
            ),
            selected_index=0,
        )

        result = sut.apply(
            action=ScrollGameroomsAction(direction=ScrollDirection.UP), state=current
        )

        assert result == expected

    def test_apply__when_down__selected_index_eq_rows_count_minus_1__does_nothing(
        self, sut: ScrollGameroomsReducer, gameroom_1, gameroom_2, gameroom_3
    ) -> None:
        current = GameroomsState(
            rows=(
                GameroomRowViewModel(gameroom=gameroom_1, is_highlighted=False),
                GameroomRowViewModel(gameroom=gameroom_2, is_highlighted=False),
                GameroomRowViewModel(gameroom=gameroom_3, is_highlighted=True),
            ),
            selected_index=2,
        )

        result = sut.apply(
            action=ScrollGameroomsAction(direction=ScrollDirection.DOWN), state=current
        )

        assert result == current

    def test_apply__when_down__selected_index_lt_rows_count_minus_1__scrolls_down(
        self, sut: ScrollGameroomsReducer, gameroom_1, gameroom_2, gameroom_3
    ) -> None:
        current = GameroomsState(
            rows=(
                GameroomRowViewModel(gameroom=gameroom_1, is_highlighted=False),
                GameroomRowViewModel(gameroom=gameroom_2, is_highlighted=True),
                GameroomRowViewModel(gameroom=gameroom_3, is_highlighted=False),
            ),
            selected_index=1,
        )
        expected = GameroomsState(
            rows=(
                GameroomRowViewModel(gameroom=gameroom_1, is_highlighted=False),
                GameroomRowViewModel(gameroom=gameroom_2, is_highlighted=False),
                GameroomRowViewModel(gameroom=gameroom_3, is_highlighted=True),
            ),
            selected_index=2,
        )

        result = sut.apply(
            action=ScrollGameroomsAction(direction=ScrollDirection.DOWN), state=current
        )

        assert result == expected
