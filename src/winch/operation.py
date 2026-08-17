"""Класс операции и поставляемый шаблон RPC."""

import json

from winch.client import Client


CONTENT_TYPE_HEADER = 'Content-Type'
HTTP_POST = 'POST'
JSON_CONTENT_TYPE = 'application/json'


class DictJsonSerializer:
    """Дефолт базы: dict через stdlib json."""

    content_type = JSON_CONTENT_TYPE

    def dumps(self, document: object) -> str:
        return json.dumps(document)

    def loads(self, body: str) -> dict:
        return json.loads(body)


def _join_url(base_url: str, path: str) -> str:
    base = base_url.rstrip('/')
    if not path:
        return base
    suffix = path if path.startswith('/') else f'/{path}'
    return f'{base}{suffix}'


class Operation:
    """База Winch: конкретный метод внешнего API."""

    client: Client | None = None
    method: str = ''
    path: str = ''
    serializer = DictJsonSerializer()

    def __init__(
        self,
        client: Client | None = None,
        **defaults: object,
    ) -> None:
        self._client = client
        self._defaults = defaults

    def __call__(self, **fields: object) -> dict:
        """Kwargs — документ тела; ответ — dict."""
        bound = self._bound_client()
        response_text = bound.adapter.send(
            self.method,
            _join_url(bound.base_url, self.path),
            self._request_headers(bound),
            self.serializer.dumps({**self._defaults, **fields}),
        )
        return self.serializer.loads(response_text)

    def _bound_client(self) -> Client:
        bound = self._client or type(self).client
        if bound is None:
            raise TypeError('client is required')
        return bound

    def _request_headers(self, bound: Client) -> dict[str, str]:
        return {
            **bound.headers,
            CONTENT_TYPE_HEADER: self.serializer.content_type,
        }


class RpcOperation(Operation):
    """Шаблон RPC: типично POST и тело."""

    method = HTTP_POST
