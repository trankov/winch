import unittest

from winch.client import Client
from winch.operation import RestOperation, RpcOperation
from winch.slots import Header, Path, Query

from recording import RecordingHttpTransport


EXAMPLE_API = 'https://api.example.test'


class GetUser(RestOperation):
    method = 'GET'
    path = '/users/{user_id}'
    user_id: Path[str]
    limit: Query[int]
    authorization: Header[str]


class Echo(RpcOperation):
    path = '/echo/{locale}'
    locale: Path[str]


class RestSlotsTests(unittest.TestCase):
    def test_rest_slots_fill_path_query_header(self) -> None:
        http_transport = RecordingHttpTransport(response='{"name": "Ada"}')
        get_user = GetUser(
            client=Client(
                http_transport=http_transport,
                base_url=EXAMPLE_API,
                headers={'X-Token': 'secret'},
            ),
        )

        reply = get_user(
            user_id='42',
            limit=10,
            authorization='Bearer x',
        )

        self.assertEqual(reply, {'name': 'Ada'})
        self.assertEqual(http_transport.method, 'GET')
        self.assertEqual(
            http_transport.url,
            f'{EXAMPLE_API}/users/42?limit=10',
        )
        self.assertEqual(http_transport.body, '')
        self.assertEqual(
            http_transport.headers,
            {
                'X-Token': 'secret',
                'authorization': 'Bearer x',
            },
        )

    def test_rpc_keeps_unannotated_in_body(self) -> None:
        http_transport = RecordingHttpTransport(response='{"ok": true}')
        echo = Echo(
            client=Client(
                http_transport=http_transport,
                base_url=EXAMPLE_API,
            ),
        )

        reply = echo(locale='en', text='hello')

        self.assertEqual(reply, {'ok': True})
        self.assertEqual(http_transport.method, 'POST')
        self.assertEqual(http_transport.url, f'{EXAMPLE_API}/echo/en')
        self.assertEqual(http_transport.body, '{"text": "hello"}')


if __name__ == '__main__':
    unittest.main()
