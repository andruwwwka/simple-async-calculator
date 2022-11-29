import functools
import logging
import time
from abc import ABC, abstractmethod
from collections.abc import Callable


class StatsTimingInterface(ABC):  # pylint: disable=too-few-public-methods
    """Интерфейс сборщика стаитстики"""

    @abstractmethod
    def collect(self, *, function_name: str, timing: float) -> None:
        """Фиксация времени выполнения в статистике"""


class LoggerStatsTiming(StatsTimingInterface):  # pylint: disable=too-few-public-methods
    """Отображение таймингов выполнения функций в логах"""

    def __init__(self):
        """Иниуиализация сборщика статистики"""
        self.logger = logging.getLogger("timings")

    def collect(self, *, function_name: str, timing: float) -> None:
        """Фиксация времени выполнения функции в логах"""
        self.logger.info("Function: %s; duration: %s", function_name, timing)


stats_timing_collector = LoggerStatsTiming()


def timer(func) -> Callable:
    """Декоратор для вычисления времени выполнения функции"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        end_time = time.perf_counter()
        stats_timing_collector.collect(
            function_name=func.__name__, timing=(end_time - start_time)
        )
        return result

    return wrapper
