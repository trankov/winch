import unittest

from tests.recording import RecordingHttpTransport
from winch.client import Client, HttpResponse
from winch.exceptions import WinchBodyException
from winch.operation import RpcOperation


EXAMPLE_API = 'https://api.example.test'
ERROR_BODY = '{"Success": false, "Message": "no funds", "Code": "E1"}'


class Echo(RpcOperation):
    path = '/echo'


class Charge(RpcOperation):
    path = '/charge'

    def read_document(
        self,
        document: object,
        http_response: HttpResponse,
    ) -> object:
        if not isinstance(document, dict):
            return document
        if document.get('Success') is not False:
            return document
        raise WinchBodyException(
            message=str(document['Message']),
            code=document['Code'],
            http_response=http_response,
        )


class ErrorInBodyTests(unittest.TestCase):
    def test_error_body_is_returned_by_default(self) -> None:
        echo = Echo(
            client=Client(
                http_transport=RecordingHttpTransport(response=ERROR_BODY),
                base_url=EXAMPLE_API,
            ),
        )

        reply = echo(text='hello')

        self.assertEqual(
            reply,
            {'Success': False, 'Message': 'no funds', 'Code': 'E1'},
        )

    def test_operation_raises_body_exception(self) -> None:
        http_transport = RecordingHttpTransport(response=ERROR_BODY)
        charge = Charge(
            client=Client(
                http_transport=http_transport,
                base_url=EXAMPLE_API,
            ),
        )

        try:
            charge(amount=10)
        except WinchBodyException as body_error:
            self.assertEqual(str(body_error), 'no funds')
            self.assertEqual(body_error.code, 'E1')
            self.assertIs(
                body_error.http_response,
                http_transport.http_response,
            )
        else:
            self.fail('WinchBodyException expected')


if __name__ == '__main__':
    unittest.main()
