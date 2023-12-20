from unittest.mock import create_autospec

import pytest
from cacheout import Cache as Cacheout  # type: ignore

from src.tuicub.common.cache import Cache


@pytest.fixture()
def cacheout() -> Cacheout:
    return create_autospec(Cacheout)


@pytest.fixture()
def sut(cacheout) -> Cache:
    return Cache(cache_engine=cacheout)


class TestGet:
    def test_returns_value_from_cache_engine(self, sut, cacheout) -> None:
        expected = "foo"
        cacheout.get.return_value = expected

        result = sut.get(key=42, default="bar")

        assert result == expected
        cacheout.get.assert_called_once_with(key=42, default="bar")


class TestSet:
    def test_stores_value_in_cache_engine(self, sut, cacheout) -> None:
        sut.set(key=42, value="foo")

        cacheout.set.assert_called_once_with(key=42, value="foo")
