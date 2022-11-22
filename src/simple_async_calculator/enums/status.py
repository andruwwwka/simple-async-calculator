from enum import Enum


class Status(str, Enum):
    """Допустимые статусы задачи"""
    PENDING = "pending"
    SUCCESS = "success"
    ERROR = "error"
