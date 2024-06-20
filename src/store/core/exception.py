from typing import Type


class BaseException(Exception):
    message: str = "Internal Server Error"

    def __init__(self, message: str | None = None) -> None:
        if message:
            self.message = message

    def __str__(self) -> str:
        return f"{type(self).__name__}: {self.message}"


class GenericException(BaseException):
    message = "Generic Exception"

    def __init__(
        self,
        message: str | None = None,
        from_exception: Type[Exception] = None,
        **kwargs,
    ) -> None:
        super().__init__(message)

        self.from_exception: Type[Exception] = from_exception
        self.details = kwargs

    def __str__(self) -> str:
        if self.from_exception:
            return f"{type(self).__name__}: {self.message} caused by {self.from_exception.__name__}. Details: {self.details}"
        else:
            return f"{type(self).__name__}: {self.message}. Details: {self.details}"


class NotFoundException(BaseException):
    message = "Not Found Exception"


class DataBaseException(GenericException):
    message = "Database Exception"
