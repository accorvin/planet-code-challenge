from enum import Enum


class ErrorType(Enum):
    user = 'USER'
    server = 'SERVER'
    not_found = 'NOTFOUND'


class ModelException(Exception):

    def __init__(self, error_type, error_message):
        self.error_type = error_type
        self.error_message = error_message
