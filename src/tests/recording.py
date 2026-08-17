"""Подставной HTTP-транспорт для тестов вызова."""

from http import HTTPStatus

from winch.client import HttpResponse


class RecordingHttpTransport:
    """Запоминает `send` и отдаёт заготовленный ответ."""

    def __init__(
        self,
        response: str,
        status: int = HTTPStatus.OK,
    ) -> None:
        self.http_response = HttpResponse(status=status, body=response)
        self.method = ''
        self.url = ''
        self.headers: dict[str, str] = {}
        self.body = ''

    def send(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: str,
    ) -> HttpResponse:
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body
        return self.http_response


class RecordingAsyncHttpTransport:
    """Запоминает async `send` и отдаёт заготовленный ответ."""

    def __init__(
        self,
        response: str,
        status: int = HTTPStatus.OK,
    ) -> None:
        self.http_response = HttpResponse(status=status, body=response)
        self.method = ''
        self.url = ''
        self.headers: dict[str, str] = {}
        self.body = ''

    async def send(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: str,
    ) -> HttpResponse:
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body
        return self.http_response


class BrokenHttpTransport:
    """Транспорт, который не выполняет запрос."""

    def send(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: str,
    ) -> HttpResponse:
        raise OSError('connection refused')
