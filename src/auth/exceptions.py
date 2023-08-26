from src.exceptions import BaseAPIException


class UserIncorrectPasswordError(BaseAPIException):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg
