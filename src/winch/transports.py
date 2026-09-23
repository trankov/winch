"""Транспорт HTTP: httpx и requests."""

from collections.abc import Mapping
from types import TracebackType
from typing import Protocol, Self

from winch.client import HttpResponse


def _body_content(body: str) -> bytes | None:
    if not body:
        return None
    return body.encode()


def _response_headers(headers: Mapping[str, str]) -> dict[str, str]:
    return {name.lower(): header for name, header in headers.items()}


class _HttpLibResponse(Protocol):
    """Ответ httpx или requests: код, текст и заголовки."""

    @property
    def status_code(self) -> int: ...

    @property
    def text(self) -> str: ...

    @property
    def headers(self) -> Mapping[str, str]: ...


class _RequestsSender(Protocol):
    """Модуль requests или Session: `request` с `data`."""

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        data: bytes | None = None,  # noqa: WPS110
    ) -> _HttpLibResponse: ...


class _HttpxSender(Protocol):
    """Модуль httpx или Client: `request` с `content`."""

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        content: bytes | None = None,  # noqa: WPS110
    ) -> _HttpLibResponse: ...


class _AsyncHttpxSender(Protocol):
    """AsyncClient: await `request` с `content`."""

    async def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        content: bytes | None = None,  # noqa: WPS110
    ) -> _HttpLibResponse: ...

    async def __aenter__(self) -> Self: ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...


class _AsyncClientFactory(Protocol):
    """Конструктор `httpx.AsyncClient` без аргументов."""

    def __call__(self) -> _AsyncHttpxSender: ...


class RequestsTransport:
    """Синхронный транспорт на requests. Библиотеку ставит автор."""

    _requests: _RequestsSender
    _requests_session: _RequestsSender | None

    def __init__(
        self,
        requests_session: _RequestsSender | None = None,
    ) -> None:
        import requests  # pyright: ignore[reportMissingModuleSource]

        self._requests = requests
        self._requests_session = requests_session

    def send(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: str,
    ) -> HttpResponse:
        sender = self._requests_session or self._requests
        http_response = sender.request(
            method=method,
            url=url,
            headers=headers,
            data=_body_content(body=body),
        )
        return HttpResponse(
            status=http_response.status_code,
            body=http_response.text,
            headers=_response_headers(headers=http_response.headers),
        )


class HttpxTransport:
    """Синхронный транспорт на httpx. Библиотеку ставит автор."""

    _httpx: _HttpxSender
    _httpx_client: _HttpxSender | None

    def __init__(self, httpx_client: _HttpxSender | None = None) -> None:
        import httpx

        self._httpx = httpx
        self._httpx_client = httpx_client

    def send(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: str,
    ) -> HttpResponse:
        sender = self._httpx_client or self._httpx
        http_response = sender.request(
            method=method,
            url=url,
            headers=headers,
            content=_body_content(body=body),
        )
        return HttpResponse(
            status=http_response.status_code,
            body=http_response.text,
            headers=_response_headers(headers=http_response.headers),
        )


class AsyncHttpxTransport:
    """Асинхронный транспорт на httpx. Библиотеку ставит автор."""

    _async_client_factory: _AsyncClientFactory
    _httpx_client: _AsyncHttpxSender | None

    def __init__(
        self,
        httpx_client: _AsyncHttpxSender | None = None,
    ) -> None:
        import httpx

        self._async_client_factory = httpx.AsyncClient
        self._httpx_client = httpx_client

    async def send(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: str,
    ) -> HttpResponse:
        bound_client = self._httpx_client
        if bound_client is not None:
            http_response = await bound_client.request(
                method=method,
                url=url,
                headers=headers,
                content=_body_content(body=body),
            )
            return HttpResponse(
                status=http_response.status_code,
                body=http_response.text,
                headers=_response_headers(headers=http_response.headers),
            )
        async with self._async_client_factory() as httpx_client:
            http_response = await httpx_client.request(
                method=method,
                url=url,
                headers=headers,
                content=_body_content(body=body),
            )
        return HttpResponse(
            status=http_response.status_code,
            body=http_response.text,
            headers=_response_headers(headers=http_response.headers),
        )
