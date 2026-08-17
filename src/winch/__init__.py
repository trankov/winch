"""Winch: операции Python над HTTP API."""

from winch.adapters import AsyncHttpxAdapter, HttpxAdapter, RequestsAdapter
from winch.client import AsyncClient, Client, HttpResponse
from winch.exceptions import WinchHttpException, WinchRefusalException
from winch.operation import RestOperation, RpcOperation
from winch.slots import Body, Header, Path, Query


__all__ = (
    'AsyncClient',
    'AsyncHttpxAdapter',
    'Body',
    'Client',
    'Header',
    'HttpResponse',
    'HttpxAdapter',
    'Path',
    'Query',
    'RequestsAdapter',
    'RestOperation',
    'RpcOperation',
    'WinchHttpException',
    'WinchRefusalException',
)
