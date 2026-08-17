"""Класс операции и поставляемые шаблоны RPC и REST."""

from http import HTTPStatus

from winch.client import AsyncClient, Client, HttpResponse
from winch.exceptions import WinchHttpException
from winch.http_call import PreparedRequest, send_async, send_sync
from winch.serializers import DictJsonSerializer
from winch.slots import (
    SlotBundle,
    collect_slot_kinds,
    split_fields,
)


CONTENT_TYPE_HEADER = 'Content-Type'
HTTP_POST = 'POST'


def _merge_headers(
    client_headers: dict[str, str],
    slot_headers: dict[str, object],
    content_type: str,
    has_body: bool,
) -> dict[str, str]:
    headers = {
        **client_headers,
        **{
            name: str(field_value)
            for name, field_value in slot_headers.items()
        },
    }
    if has_body:
        headers[CONTENT_TYPE_HEADER] = content_type
    return headers


def _status_is_success(
    status: int,
    success_statuses: frozenset[int] | None,
) -> bool:
    if success_statuses is None:
        return HTTPStatus.OK <= status < HTTPStatus.MULTIPLE_CHOICES
    return status in success_statuses


class Operation:
    """База Winch: конкретный метод внешнего API."""

    client: Client | AsyncClient | None = None
    method: str = ''
    path: str = ''
    serializer = DictJsonSerializer()
    success_statuses: frozenset[int] | None = None

    def __init__(
        self,
        client: Client | AsyncClient | None = None,
        **defaults: object,
    ) -> None:
        self._client = client
        self._defaults = defaults

    def __call__(self, **fields: object) -> object:
        """Kwargs — слоты и документ тела; ответ — объект сериализатора."""
        bound_client = self._bound_client()
        prepared_request = self._prepare_request(
            bound_client=bound_client,
            fields=fields,
        )
        if isinstance(bound_client, AsyncClient):
            return self._call_async(
                bound_client=bound_client,
                prepared_request=prepared_request,
            )
        return self._read_body(
            http_response=send_sync(
                http_transport=bound_client.http_transport,
                prepared_request=prepared_request,
            ),
        )

    async def _call_async(
        self,
        bound_client: AsyncClient,
        prepared_request: PreparedRequest,
    ) -> object:
        http_response = await send_async(
            http_transport=bound_client.http_transport,
            prepared_request=prepared_request,
        )
        return self._read_body(http_response=http_response)

    def _bound_client(self) -> Client | AsyncClient:
        bound_client = self._client or type(self).client
        if bound_client is None:
            raise TypeError('client is required')
        return bound_client

    def _prepare_request(
        self,
        bound_client: Client | AsyncClient,
        fields: dict[str, object],
    ) -> PreparedRequest:
        slot_bundle = split_fields(
            slot_kinds=collect_slot_kinds(operation_type=type(self)),
            merged={**self._defaults, **fields},
        )
        body = self._body_text(slot_bundle=slot_bundle)
        return PreparedRequest(
            method=self.method,
            url=slot_bundle.url(
                base_url=bound_client.base_url,
                path=self.path,
            ),
            headers=_merge_headers(
                client_headers=bound_client.headers,
                slot_headers=slot_bundle.header,
                content_type=self.serializer.content_type,
                has_body=bool(body),
            ),
            body=body,
        )

    def _body_text(self, slot_bundle: SlotBundle) -> str:
        if isinstance(self, RestOperation):
            return ''
        return self.serializer.dumps(slot_bundle.body)

    def _read_body(self, http_response: HttpResponse) -> object:
        if not _status_is_success(
            status=http_response.status,
            success_statuses=self.success_statuses,
        ):
            raise WinchHttpException(http_response=http_response)
        return self.serializer.loads(http_response.body)


class RpcOperation(Operation):
    """Шаблон RPC: типично POST и тело."""

    method = HTTP_POST


class RestOperation(Operation):
    """Шаблон REST: HTTP-метод задаёт каждая операция."""
