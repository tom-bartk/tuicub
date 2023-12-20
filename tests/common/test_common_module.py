import pytest

from src.tuicub.common.cache import Cache
from src.tuicub.common.logger import Logger
from src.tuicub.common.module import CommonModule


@pytest.fixture()
def sut(config, theme) -> CommonModule:
    return CommonModule(config=config, theme=theme)


class TestCommonModule:
    def test_config__returns_instance_from_init(self, sut, config) -> None:
        expected = config
        result = sut.config

        assert result == expected

    def test_theme__returns_instance_from_init(self, sut, theme) -> None:
        expected = theme
        result = sut.theme

        assert result == expected

    def test_logger__returns_logger_instance(self, sut) -> None:
        result = sut.logger

        assert isinstance(result, Logger)

    def test_cache__returns_cache_instance(self, sut) -> None:
        result = sut.cache()

        assert isinstance(result, Cache)
