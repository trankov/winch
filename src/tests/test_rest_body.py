import unittest

from tests.recording import RecordingHttpTransport
from winch.client import Client
from winch.operation import RestOperation
from winch.slots import Body, Path


EXAMPLE_API = 'https://api.example.test'


class PatchUser(RestOperation):
    method = 'PATCH'
    path = '/users/{user_id}'
    user_id: Path[str]
    patch: Body[dict]


class RestBodyTests(unittest.TestCase):
    def test_rest_sends_one_nested_body_document(self) -> None:
        http_transport = RecordingHttpTransport(response='{"ok": true}')
        patch_user = PatchUser(
            client=Client(
                http_transport=http_transport,
                base_url=EXAMPLE_API,
            ),
        )

        reply = patch_user(
            user_id='42',
            patch={'profile': {'name': 'Ada'}},
        )

        self.assertEqual(reply, {'ok': True})
        self.assertEqual(http_transport.method, 'PATCH')
        self.assertEqual(http_transport.url, f'{EXAMPLE_API}/users/42')
        self.assertEqual(
            http_transport.body,
            '{"profile": {"name": "Ada"}}',
        )
        self.assertEqual(
            http_transport.headers['Content-Type'],
            'application/json',
        )


if __name__ == '__main__':
    unittest.main()
