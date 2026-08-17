"""Клиент внешнего API: HTTP-транспорт, база URL и заголовки."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Protocol


@dataclass(slots=True)
class HttpResponse:
    """Ответ транспорта: статус и строка тела."""

    status: int
    body: str


class HttpTransportAdapter(Protocol):
    """Синхронный адаптер HTTP-транспорта."""

    def send(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: str,
    ) -> HttpResponse:
        """Отправить собранный запрос и вернуть статус с телом."""
        ...


class AsyncHttpTransportAdapter(Protocol):
    """Асинхронный адаптер HTTP-транспорта."""

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
        http_transport: HttpTransportAdapter,
    ) -> HttpTransportAdapter:
        """Обернуть синхронный транспорт."""
        ...

    def wrap_async(
        self,
        http_transport: AsyncHttpTransportAdapter,
    ) -> AsyncHttpTransportAdapter:
        """Обернуть асинхронный транспорт."""
        ...


class Client:
    """Синхронный живой экземпляр для одного внешнего API."""

    def __init__(
        self,
        http_transport: HttpTransportAdapter,
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
        http_transport: AsyncHttpTransportAdapter,
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
