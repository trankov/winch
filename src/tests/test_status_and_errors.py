import unittest
from http import HTTPStatus

from tests.recording import BrokenHttpTransport, RecordingHttpTransport
from winch.client import Client
from winch.exceptions import WinchHttpException, WinchNetworkException
from winch.operation import RpcOperation


EXAMPLE_API = 'https://api.example.test'


class Echo(RpcOperation):
    path = '/echo'


class AddUser(RpcOperation):
    path = '/add_user'
    success_statuses = frozenset((HTTPStatus.CREATED,))


class DeleteItem(RpcOperation):
    method = 'DELETE'
    path = '/items'
    success_statuses = frozenset(
        (
            *range(HTTPStatus.OK, HTTPStatus.MULTIPLE_CHOICES),
            HTTPStatus.GONE,
        )
    )


class StatusAndErrorsTests(unittest.TestCase):
    def test_any_2xx_reads_body(self) -> None:
        http_transport = RecordingHttpTransport(
            response='{"ok": true}',
            status=HTTPStatus.ACCEPTED,
        )
        echo = Echo(
            client=Client(
                http_transport=http_transport,
                base_url=EXAMPLE_API,
            ),
        )

        reply = echo(text='hello')

        self.assertEqual(reply, {'ok': True})

    def test_narrow_success_rejects_ok_as_http_error(self) -> None:
        http_transport = RecordingHttpTransport(
            response='{"id": 1}',
            status=HTTPStatus.OK,
        )
        add_user = AddUser(
            client=Client(
                http_transport=http_transport,
                base_url=EXAMPLE_API,
            ),
        )

        try:
            add_user(name='Ada')
        except WinchHttpException as http_error:
            self.assertIs(
                http_error.http_response,
                http_transport.http_response,
            )
            self.assertNotIsInstance(http_error, WinchNetworkException)
        else:
            self.fail('WinchHttpException expected')

    def test_widened_success_reads_gone_body(self) -> None:
        http_transport = RecordingHttpTransport(
            response='{"deleted": true}',
            status=HTTPStatus.GONE,
        )
        delete_item = DeleteItem(
            client=Client(
                http_transport=http_transport,
                base_url=EXAMPLE_API,
            ),
        )

        reply = delete_item()

        self.assertEqual(reply, {'deleted': True})

    def test_transport_failure_is_network_error(self) -> None:
        echo = Echo(
            client=Client(
                http_transport=BrokenHttpTransport(),
                base_url=EXAMPLE_API,
            ),
        )

        try:
            echo(text='hello')
        except WinchNetworkException as network_error:
            self.assertNotIsInstance(network_error, WinchHttpException)
        else:
            self.fail('WinchNetworkException expected')


if __name__ == '__main__':
    unittest.main()
