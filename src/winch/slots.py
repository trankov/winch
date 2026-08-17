"""Слоты path, query, header и один документ тела."""

from typing import get_origin
from urllib.parse import quote, urlencode


class Path[Scalar]:
    """Слот пути: скаляр в сегмент URL."""


class Query[Scalar]:
    """Слот query: скаляр в строку запроса."""


class Header[Scalar]:
    """Слот заголовка: скаляр в заголовок запроса."""


class Body[Document]:
    """Слот тела: один документ, не склейка полей."""


class SlotBundle:
    """Аргументы вызова, разложенные по слотам HTTP."""

    def __init__(self) -> None:
        self.path: dict[str, object] = {}
        self.query: dict[str, object] = {}
        self.header: dict[str, object] = {}
        self.body: dict[str, object] = {}
        self.document: object | None = None

    def url(self, base_url: str, path: str) -> str:
        """База клиента, путь со слотами и строка query."""
        joined = self._join_base(
            base_url=base_url,
            path=self._filled_path(path=path),
        )
        return f'{joined}{self._query_suffix()}'

    def take(
        self,
        slot_kinds: dict[str, type],
        merged: dict[str, object],
    ) -> None:
        targets = {
            Path: self.path,
            Query: self.query,
            Header: self.header,
        }
        for name, field_value in merged.items():
            kind = slot_kinds.get(name)
            if kind is Body:
                self._put_document(field_value=field_value)
                continue
            if kind is None:
                self.body[name] = field_value
                continue
            targets[kind][name] = field_value

    def _put_document(self, field_value: object) -> None:
        if self.document is not None:
            raise TypeError('only one Body document')
        self.document = field_value

    def _filled_path(self, path: str) -> str:
        return path.format(
            **{
                name: quote(str(field_value), safe='')
                for name, field_value in self.path.items()
            },
        )

    def _join_base(self, base_url: str, path: str) -> str:
        base = base_url.rstrip('/')
        if not path:
            return base
        suffix = path if path.startswith('/') else f'/{path}'
        return f'{base}{suffix}'

    def _query_suffix(self) -> str:
        if not self.query:
            return ''
        encoded = urlencode(
            {
                name: str(field_value)
                for name, field_value in self.query.items()
            }
        )
        return f'?{encoded}'


def _slot_kinds(operation_type: type) -> dict[str, type]:
    collected: dict[str, type] = {}
    for ancestor in reversed(operation_type.__mro__):
        for name, annotation in getattr(
            ancestor,
            '__annotations__',
            {},
        ).items():
            origin = get_origin(annotation) or annotation
            if origin in {Path, Query, Header, Body}:
                collected[name] = origin
    return collected


def split_fields(
    operation_type: type,
    merged: dict[str, object],
) -> SlotBundle:
    """Разложить kwargs: слоты отдельно, остальное — тело."""
    slot_bundle = SlotBundle()
    slot_bundle.take(
        slot_kinds=_slot_kinds(operation_type=operation_type),
        merged=merged,
    )
    return slot_bundle
