"""Поставляемые адаптеры к requests и httpx."""

from winch.client import HttpResponse


def _body_content(body: str) -> bytes | None:
    if not body:
        return None
    return body.encode()


class RequestsAdapter:
    """Синхронный адаптер к requests. Библиотеку ставит автор."""

    _requests: object
    _requests_session: object | None

    def __init__(self, requests_session: object | None = None) -> None:
        import requests

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
        )


class HttpxAdapter:
    """Синхронный адаптер к httpx. Библиотеку ставит автор."""

    _httpx: object
    _httpx_client: object | None

    def __init__(self, httpx_client: object | None = None) -> None:
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
        )


class AsyncHttpxAdapter:
    """Асинхронный адаптер к httpx. Библиотеку ставит автор."""

    _httpx: object
    _httpx_client: object | None

    def __init__(self, httpx_client: object | None = None) -> None:
        import httpx

        self._httpx = httpx
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
            )
        async with self._httpx.AsyncClient() as httpx_client:
            http_response = await httpx_client.request(
                method=method,
                url=url,
                headers=headers,
                content=_body_content(body=body),
            )
        return HttpResponse(
            status=http_response.status_code,
            body=http_response.text,
        )
