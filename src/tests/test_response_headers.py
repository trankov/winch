import unittest
from http import HTTPStatus

from winch.client import Client
from winch.exceptions import WinchHttpException
from winch.operation import RpcOperation
from winch.transports import HttpxTransport

import httpx


EXAMPLE_API = 'https://api.example.test/v1'


class Echo(RpcOperation):
    path = '/echo'


def _refusing(request: httpx.Request) -> httpx.Response:
    return httpx.Response(
        status_code=HTTPStatus.FORBIDDEN,
        headers=[
            ('X-Sp-Crid', 'abc-123'),
            ('Set-Cookie', 'spid=1; Path=/'),
            ('Set-Cookie', 'spsc=2; Path=/'),
        ],
        text='<h1>Forbidden</h1>',
    )


class ResponseHeadersTests(unittest.TestCase):
    def test_refusal_carries_headers(self) -> None:
        echo = Echo(
            client=Client(
                http_transport=HttpxTransport(
                    httpx_client=httpx.Client(
                        transport=httpx.MockTransport(_refusing),
                    ),
                ),
                base_url=EXAMPLE_API,
            ),
        )

        try:
            echo(text='hello')
        except WinchHttpException as refusal:
            headers = refusal.http_response.headers
        else:
            self.fail('отказ не поднят')
        self.assertEqual(headers['x-sp-crid'], 'abc-123')
        self.assertEqual(
            headers['set-cookie'],
            'spid=1; Path=/, spsc=2; Path=/',
        )


if __name__ == '__main__':
    unittest.main()
