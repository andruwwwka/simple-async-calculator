from enum import Enum


class Status(str, Enum):
    pending = 'pending'
    success = 'success'
    error = 'error'
