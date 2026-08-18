"""Плагины клиента: повтор запроса, не ядро операции."""

from winch.client import AsyncHttpTransport, HttpResponse, HttpTransport


_RETRY_ATTEMPTS = 2


class _RetryingHttpTransport:
    def __init__(
        self,
        http_transport: HttpTransport,
        attempts: int,
    ) -> None:
        self._http_transport = http_transport
        self._attempts = attempts

    def send(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: str,
    ) -> HttpResponse:
        remaining = self._attempts
        while True:
            remaining -= 1
            try:
                return self._http_transport.send(
                    method=method,
                    url=url,
                    headers=headers,
                    body=body,
                )
            except OSError:
                if remaining <= 0:
                    raise


class _RetryingAsyncHttpTransport:
    def __init__(
        self,
        http_transport: AsyncHttpTransport,
        attempts: int,
    ) -> None:
        self._http_transport = http_transport
        self._attempts = attempts

    async def send(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: str,
    ) -> HttpResponse:
        remaining = self._attempts
        while True:
            remaining -= 1
            try:
                return await self._http_transport.send(
                    method=method,
                    url=url,
                    headers=headers,
                    body=body,
                )
            except OSError:
                if remaining <= 0:
                    raise


class RetryPlugin:
    """Простой повтор `send` на клиенте."""

    def wrap_sync(
        self,
        http_transport: HttpTransport,
    ) -> HttpTransport:
        return _RetryingHttpTransport(
            http_transport=http_transport,
            attempts=_RETRY_ATTEMPTS,
        )

    def wrap_async(
        self,
        http_transport: AsyncHttpTransport,
    ) -> AsyncHttpTransport:
        return _RetryingAsyncHttpTransport(
            http_transport=http_transport,
            attempts=_RETRY_ATTEMPTS,
        )
