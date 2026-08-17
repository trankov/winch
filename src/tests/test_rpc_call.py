import unittest

from tests.recording import RecordingHttpTransport
from winch.client import Client
from winch.operation import Operation, RpcOperation


class Echo(RpcOperation):
    path = '/echo'


class Payout(RpcOperation):
    path = '/payout'


class TemplatedEcho(RpcOperation):
    path = '/echo'


class BareOperation(Operation):
    method = 'POST'
    path = '/bare'


class RpcCallTests(unittest.TestCase):
    def test_rpc_call_posts_body_and_returns_dict(self) -> None:
        http_transport = RecordingHttpTransport(response='{"ok": true}')
        client = Client(
            http_transport=http_transport,
            base_url='https://api.example.test/v1',
            headers={'X-Token': 'secret'},
        )
        echo = Echo(client=client)

        reply = echo(text='hello')

        self.assertEqual(reply, {'ok': True})
        self.assertEqual(http_transport.method, 'POST')
        self.assertEqual(
            http_transport.url,
            'https://api.example.test/v1/echo',
        )
        self.assertEqual(http_transport.body, '{"text": "hello"}')
        self.assertEqual(
            http_transport.headers,
            {
                'X-Token': 'secret',
                'Content-Type': 'application/json',
            },
        )

    def test_two_instances_keep_init_defaults(self) -> None:
        http_transport = RecordingHttpTransport(response='{"id": 1}')
        client = Client(
            http_transport=http_transport,
            base_url='https://api.example.test',
        )
        regular = Payout(client=client, kind='regular')
        taxed = Payout(client=client, kind='tax')

        regular(amount=10)

        self.assertEqual(
            http_transport.body,
            '{"kind": "regular", "amount": 10}',
        )

        taxed(amount=10)

        self.assertEqual(
            http_transport.body,
            '{"kind": "tax", "amount": 10}',
        )

    def test_template_client_replaced_by_assignment(self) -> None:
        first = RecordingHttpTransport(response='{"n": 1}')
        second = RecordingHttpTransport(response='{"n": 2}')
        TemplatedEcho.client = Client(
            http_transport=first,
            base_url='https://first.example.test',
        )
        echo = TemplatedEcho()

        echo(text='a')

        self.assertEqual(first.body, '{"text": "a"}')
        self.assertEqual(first.url, 'https://first.example.test/echo')

        TemplatedEcho.client = Client(
            http_transport=second,
            base_url='https://second.example.test',
        )
        echo(text='b')

        self.assertEqual(second.body, '{"text": "b"}')
        self.assertEqual(second.url, 'https://second.example.test/echo')

    def test_inheriting_base_operation_is_allowed(self) -> None:
        http_transport = RecordingHttpTransport(response='{"ok": true}')
        client = Client(
            http_transport=http_transport,
            base_url='https://api.example.test',
        )
        bare = BareOperation(client=client)

        reply = bare(flag=True)

        self.assertEqual(reply, {'ok': True})
        self.assertEqual(http_transport.method, 'POST')
        self.assertEqual(http_transport.body, '{"flag": true}')


if __name__ == '__main__':
    unittest.main()
