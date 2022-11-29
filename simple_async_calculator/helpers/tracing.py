import logging
from collections import defaultdict
from pprint import pformat
from typing import Any

tracing_logger = logging.getLogger("tracing")

full_trace: dict[int, list[dict[str, Any]]] = defaultdict(list)


class InMemoryTracing:
    """Логика трейса событий для объектов задач"""

    def __init__(self, task_id: int) -> None:
        """Инициализация трейсера"""
        self.task_id = task_id

    def add_event(self, message: dict[str, Any]) -> None:
        """Отправка события в трейс"""
        self.task_trace.append(message)

    def __enter__(self):
        """Точка входа в контекстный менеджер"""
        self.task_trace = full_trace[  # pylint: disable=attribute-defined-outside-init
            self.task_id
        ]
        return self

    def __exit__(self, exc_type, exc_value, trace):
        """При выходе из контекстного менеджера выводится весь трейс объекта в логгер"""
        tracing_logger.info(
            "Full trace for Task(%s):\n %s", self.task_id, pformat(self.task_trace)
        )
