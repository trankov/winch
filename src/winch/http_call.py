"""Собранный HTTP-запрос и отправка через адаптер."""

from winch.client import (
    AsyncHttpTransportAdapter,
    HttpResponse,
    HttpTransportAdapter,
)
from winch.exceptions import WinchNetworkException


class PreparedRequest:
    """Поля, которые уходят в `send`."""

    def __init__(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: str,
    ) -> None:
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body


def send_sync(
    http_transport: HttpTransportAdapter,
    prepared_request: PreparedRequest,
) -> HttpResponse:
    """Синхронный `send`; сбой транспорта — ошибка сети."""
    try:
        return http_transport.send(
            method=prepared_request.method,
            url=prepared_request.url,
            headers=prepared_request.headers,
            body=prepared_request.body,
        )
    except OSError as error:
        raise WinchNetworkException(str(error)) from error


async def send_async(
    http_transport: AsyncHttpTransportAdapter,
    prepared_request: PreparedRequest,
) -> HttpResponse:
    """Асинхронный `send`; сбой транспорта — ошибка сети."""
    try:
        return await http_transport.send(
            method=prepared_request.method,
            url=prepared_request.url,
            headers=prepared_request.headers,
            body=prepared_request.body,
        )
    except OSError as error:
        raise WinchNetworkException(str(error)) from error
