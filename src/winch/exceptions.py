"""Исключения этажей сети и HTTP."""

from winch.client import HttpResponse


class WinchNetworkException(Exception):
    """Сбой транспорта: запрос не выполнен."""


class WinchHttpException(Exception):
    """Статус ответа вне успешных статусов операции."""

    def __init__(self, http_response: HttpResponse) -> None:
        self.http_response = http_response
        super().__init__(f'HTTP {http_response.status}')
