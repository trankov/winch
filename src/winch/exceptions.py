"""Исключения этажей сети, HTTP и отказа в теле."""

from winch.client import HttpResponse


class WinchNetworkException(Exception):
    """Сбой транспорта: запрос не выполнен."""

    message: str

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class WinchHttpException(Exception):
    """Статус ответа вне успешных статусов операции."""

    message: str
    http_response: HttpResponse

    def __init__(self, http_response: HttpResponse) -> None:
        self.http_response = http_response
        super().__init__(f'HTTP {http_response.status}')


class WinchRefusalException(Exception):
    """Отказ в теле ответа при успешном HTTP-статусе."""

    message: str
    code: str | int
    http_response: HttpResponse

    def __init__(
        self,
        message: str,
        code: str | int,
        http_response: HttpResponse,
    ) -> None:
        self.code = code
        self.http_response = http_response
        super().__init__(message)
