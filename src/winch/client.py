"""Клиент внешнего API: HTTP-транспорт, база URL и заголовки."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Protocol


@dataclass(slots=True)
class HttpResponse:
    """Ответ транспорта: статус, строка тела и заголовки."""

    status: int
    body: str
    # Имена заголовков в нижнем регистре: так их отдаёт httpx, и так
    # один поиск находит заголовок у любого транспорта. Повторённый
    # заголовок приходит одной строкой через запятую. Пустой словарь
    # по умолчанию — у транспорта автора, который заголовков не
    # собирает.
    headers: dict[str, str] = field(default_factory=dict)


class HttpTransport(Protocol):
    """Синхронный HTTP-транспорт: обязателен `send`."""

    def send(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: str,
    ) -> HttpResponse:
        """Отправить собранный запрос и вернуть статус с телом."""
        ...


class AsyncHttpTransport(Protocol):
    """Асинхронный HTTP-транспорт: обязателен `send`."""

    async def send(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: str,
    ) -> HttpResponse:
        """Отправить собранный запрос и вернуть статус с телом."""
        ...


class ClientPlugin(Protocol):
    """Плагин клиента: оборачивает `send`, не операцию."""

    def wrap_sync(
        self,
        http_transport: HttpTransport,
    ) -> HttpTransport: ...

    def wrap_async(
        self,
        http_transport: AsyncHttpTransport,
    ) -> AsyncHttpTransport: ...


class Client:
    """Синхронный живой экземпляр для одного внешнего API."""

    def __init__(
        self,
        http_transport: HttpTransport,
        base_url: str,
        headers: Mapping[str, str] | None = None,
        plugins: Sequence[ClientPlugin] = (),
    ) -> None:
        bound_transport = http_transport
        for plugin in plugins:
            bound_transport = plugin.wrap_sync(http_transport=bound_transport)
        self.http_transport = bound_transport
        self.base_url = base_url
        self.headers = dict(headers or {})


class AsyncClient:
    """Асинхронный живой экземпляр для одного внешнего API."""

    def __init__(
        self,
        http_transport: AsyncHttpTransport,
        base_url: str,
        headers: Mapping[str, str] | None = None,
        plugins: Sequence[ClientPlugin] = (),
    ) -> None:
        bound_transport = http_transport
        for plugin in plugins:
            bound_transport = plugin.wrap_async(http_transport=bound_transport)
        self.http_transport = bound_transport
        self.base_url = base_url
        self.headers = dict(headers or {})
