from cacheout import Cache as Cacheout  # type: ignore

from .cache import Cache
from .config import Config
from .logger import Logger
from .views.color import Theme


class CommonModule:
    __slots__ = ("_config", "_logger", "_theme")

    @property
    def config(self) -> Config:
        return self._config

    @property
    def logger(self) -> Logger:
        return self._logger

    @property
    def theme(self) -> Theme:
        return self._theme

    def __init__(self, config: Config, theme: Theme):
        self._config: Config = config
        self._theme: Theme = theme

        logger = Logger(logfile_path=config.logfile, debug=config.debug)
        logger.configure()
        self._logger: Logger = logger

    def cache(self) -> Cache:
        return Cache(cache_engine=Cacheout(maxsize=1024))
