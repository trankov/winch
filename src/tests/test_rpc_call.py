import unittest

from winch.client import Client
from winch.operation import Operation, RpcOperation


class RecordingAdapter:
    """Обычный адаптер: запоминает аргументы `send` и отдаёт тело."""

    def __init__(self, response: str) -> None:
        self.response = response
        self.method = ''
        self.url = ''
        self.headers: dict[str, str] = {}
        self.body = ''

    def send(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: str,
    ) -> str:
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body
        return self.response


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
        adapter = RecordingAdapter(response='{"ok": true}')
        client = Client(
            adapter=adapter,
            base_url='https://api.example.test/v1',
            headers={'X-Token': 'secret'},
        )
        echo = Echo(client=client)

        reply = echo(text='hello')

        self.assertEqual(reply, {'ok': True})
        self.assertEqual(adapter.method, 'POST')
        self.assertEqual(adapter.url, 'https://api.example.test/v1/echo')
        self.assertEqual(adapter.body, '{"text": "hello"}')
        self.assertEqual(
            adapter.headers,
            {
                'X-Token': 'secret',
                'Content-Type': 'application/json',
            },
        )

    def test_two_instances_keep_init_defaults(self) -> None:
        adapter = RecordingAdapter(response='{"id": 1}')
        client = Client(
            adapter=adapter,
            base_url='https://api.example.test',
        )
        regular = Payout(client=client, kind='regular')
        taxed = Payout(client=client, kind='tax')

        regular(amount=10)

        self.assertEqual(
            adapter.body,
            '{"kind": "regular", "amount": 10}',
        )

        taxed(amount=10)

        self.assertEqual(adapter.body, '{"kind": "tax", "amount": 10}')

    def test_template_client_replaced_by_assignment(self) -> None:
        first = RecordingAdapter(response='{"n": 1}')
        second = RecordingAdapter(response='{"n": 2}')
        TemplatedEcho.client = Client(
            adapter=first,
            base_url='https://first.example.test',
        )
        echo = TemplatedEcho()

        echo(text='a')

        self.assertEqual(first.body, '{"text": "a"}')
        self.assertEqual(first.url, 'https://first.example.test/echo')

        TemplatedEcho.client = Client(
            adapter=second,
            base_url='https://second.example.test',
        )
        echo(text='b')

        self.assertEqual(second.body, '{"text": "b"}')
        self.assertEqual(second.url, 'https://second.example.test/echo')

    def test_inheriting_base_operation_is_allowed(self) -> None:
        adapter = RecordingAdapter(response='{"ok": true}')
        client = Client(
            adapter=adapter,
            base_url='https://api.example.test',
        )
        bare = BareOperation(client=client)

        reply = bare(flag=True)

        self.assertEqual(reply, {'ok': True})
        self.assertEqual(adapter.method, 'POST')
        self.assertEqual(adapter.body, '{"flag": true}')


if __name__ == '__main__':
    unittest.main()
