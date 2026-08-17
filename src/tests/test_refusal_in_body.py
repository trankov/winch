import unittest

from tests.recording import RecordingHttpTransport
from winch.client import Client, HttpResponse
from winch.exceptions import WinchRefusalException
from winch.operation import RpcOperation


EXAMPLE_API = 'https://api.example.test'
REFUSED_BODY = '{"Success": false, "Message": "no funds", "Code": "E1"}'


class Echo(RpcOperation):
    path = '/echo'


class Charge(RpcOperation):
    path = '/charge'

    def read_document(
        self,
        document: object,
        http_response: HttpResponse,
    ) -> object:
        payload = document if isinstance(document, dict) else {}
        if payload.get('Success') is not False:
            return document
        raise WinchRefusalException(
            message=str(payload['Message']),
            code=payload['Code'],
            http_response=http_response,
        )


class RefusalInBodyTests(unittest.TestCase):
    def test_refusal_body_is_returned_by_default(self) -> None:
        echo = Echo(
            client=Client(
                http_transport=RecordingHttpTransport(response=REFUSED_BODY),
                base_url=EXAMPLE_API,
            ),
        )

        reply = echo(text='hello')

        self.assertEqual(
            reply,
            {'Success': False, 'Message': 'no funds', 'Code': 'E1'},
        )

    def test_operation_turns_refusal_into_exception(self) -> None:
        http_transport = RecordingHttpTransport(response=REFUSED_BODY)
        charge = Charge(
            client=Client(
                http_transport=http_transport,
                base_url=EXAMPLE_API,
            ),
        )

        try:
            charge(amount=10)
        except WinchRefusalException as refused:
            self.assertEqual(str(refused), 'no funds')
            self.assertEqual(refused.code, 'E1')
            self.assertIs(
                refused.http_response,
                http_transport.http_response,
            )
        else:
            self.fail('WinchRefusalException expected')


if __name__ == '__main__':
    unittest.main()
