"""Клиент внешнего API: адаптер, база URL и общие заголовки."""

from collections.abc import Mapping
from typing import Protocol


class Adapter(Protocol):
    """Слой над транспортом. Для этого среза обязателен `send`."""

    def send(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: str,
    ) -> str:
        """Отправить собранный запрос и вернуть тело ответа."""
        ...


class Client:
    """Живой экземпляр для одного внешнего API."""

    def __init__(
        self,
        adapter: Adapter,
        base_url: str,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        self.adapter = adapter
        self.base_url = base_url
        self.headers = dict(headers or {})
