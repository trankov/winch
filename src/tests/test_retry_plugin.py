import unittest
from http import HTTPStatus

from winch.client import AsyncClient, Client, HttpResponse
from winch.exceptions import WinchNetworkException
from winch.operation import RpcOperation
from winch.plugins import RetryPlugin


EXAMPLE_API = 'https://api.example.test'


class Echo(RpcOperation):
    path = '/echo'


class FlakyHttpTransport:
    def __init__(self) -> None:
        self.sends = 0
        self.bodies: list[str] = []

    def send(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: str,
    ) -> HttpResponse:
        self.sends += 1
        self.bodies.append(body)
        if self.sends == 1:
            raise OSError('temporary failure')
        return HttpResponse(status=HTTPStatus.OK, body='{"ok": true}')


class FlakyAsyncHttpTransport:
    def __init__(self) -> None:
        self.sends = 0

    async def send(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: str,
    ) -> HttpResponse:
        self.sends += 1
        if self.sends == 1:
            raise OSError('temporary failure')
        return HttpResponse(status=HTTPStatus.OK, body='{"ok": true}')


class RetryPluginTests(unittest.TestCase):
    def test_no_plugin_fails_after_one_send(self) -> None:
        http_transport = FlakyHttpTransport()
        echo = Echo(
            client=Client(
                http_transport=http_transport,
                base_url=EXAMPLE_API,
            ),
        )

        try:
            echo(text='hello')
        except WinchNetworkException:
            self.assertEqual(http_transport.sends, 1)
        else:
            self.fail('WinchNetworkException expected')

    def test_retry_plugin_repeats_send_from_the_call(self) -> None:
        http_transport = FlakyHttpTransport()
        echo = Echo(
            client=Client(
                http_transport=http_transport,
                base_url=EXAMPLE_API,
                plugins=(RetryPlugin(),),
            ),
        )

        reply = echo(text='hello')

        self.assertEqual(reply, {'ok': True})
        self.assertEqual(http_transport.sends, 2)
        self.assertEqual(
            http_transport.bodies,
            ['{"text": "hello"}', '{"text": "hello"}'],
        )


class AsyncRetryPluginTests(unittest.IsolatedAsyncioTestCase):
    async def test_retry_plugin_repeats_async_send(self) -> None:
        http_transport = FlakyAsyncHttpTransport()
        echo = Echo(
            client=AsyncClient(
                http_transport=http_transport,
                base_url=EXAMPLE_API,
                plugins=(RetryPlugin(),),
            ),
        )

        reply = await echo(text='hello')  # pyright: ignore[reportGeneralTypeIssues]

        self.assertEqual(reply, {'ok': True})
        self.assertEqual(http_transport.sends, 2)


if __name__ == '__main__':
    unittest.main()
