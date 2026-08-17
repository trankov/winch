import inspect
import unittest

from tests.recording import RecordingAsyncHttpTransport, RecordingHttpTransport
from winch.client import AsyncClient, Client
from winch.operation import RpcOperation


EXAMPLE_API = 'https://api.example.test/v1'


class Echo(RpcOperation):
    path = '/echo'


class AsyncClientTests(unittest.IsolatedAsyncioTestCase):
    async def test_await_echo_posts_same_request(self) -> None:
        http_transport = RecordingAsyncHttpTransport(response='{"ok": true}')
        echo = Echo(
            client=AsyncClient(
                http_transport=http_transport,
                base_url=EXAMPLE_API,
                headers={'X-Token': 'secret'},
            ),
        )

        reply = await echo(text='hello')  # pyright: ignore[reportGeneralTypeIssues]

        self.assertEqual(reply, {'ok': True})
        self.assertEqual(http_transport.method, 'POST')
        self.assertEqual(http_transport.url, f'{EXAMPLE_API}/echo')
        self.assertEqual(http_transport.body, '{"text": "hello"}')
        self.assertEqual(
            http_transport.headers,
            {
                'X-Token': 'secret',
                'Content-Type': 'application/json',
            },
        )

    def test_sync_async_are_separate_types(self) -> None:
        sync_client = Client(
            http_transport=RecordingHttpTransport(response='{}'),
            base_url=EXAMPLE_API,
        )
        async_client = AsyncClient(
            http_transport=RecordingAsyncHttpTransport(response='{}'),
            base_url=EXAMPLE_API,
        )
        pending = Echo(client=async_client)(text='hello')

        self.assertEqual(Echo(client=sync_client)(text='hello'), {})
        self.assertTrue(inspect.iscoroutine(pending))
        self.assertNotIsInstance(sync_client, AsyncClient)
        self.assertNotIsInstance(async_client, Client)
        pending.close()  # pyright: ignore[reportAttributeAccessIssue]


if __name__ == '__main__':
    unittest.main()
