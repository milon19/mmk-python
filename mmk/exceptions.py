class MmkAPIException(Exception):
    """Mmk API base exception"""

    def __init__(self, message: str, status_code: int = None, data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.data = data


class MmkConnectionError(MmkAPIException):
    """Mmk connection exception"""
    pass
