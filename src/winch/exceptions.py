"""Исключения этажей сети, HTTP и отказа в теле."""

from winch.client import HttpResponse


class WinchNetworkException(Exception):
    """Сбой транспорта: запрос не выполнен."""


class WinchHttpException(Exception):
    """Статус ответа вне успешных статусов операции."""

    def __init__(self, http_response: HttpResponse) -> None:
        self.http_response = http_response
        super().__init__(f'HTTP {http_response.status}')


class WinchRefusalException(Exception):
    """Отказ в теле ответа при успешном HTTP-статусе."""

    def __init__(
        self,
        message: str,
        code: object,
        http_response: HttpResponse,
    ) -> None:
        self.code = code
        self.http_response = http_response
        super().__init__(message)
