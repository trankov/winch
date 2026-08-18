import unittest
from dataclasses import dataclass
from typing import TypedDict

from tests.recording import RecordingHttpTransport
from winch.client import Client
from winch.operation import RpcOperation
from winch.serializers import (
    DataclassJsonSerializer,
    DictJsonSerializer,
    TypedDictJsonSerializer,
)


EXAMPLE_API = 'https://api.example.test'
PIPE_CONTENT_TYPE = 'text/plain'


@dataclass
class EchoDoc:
    text: str


class EchoTyped(TypedDict):
    text: str


class PipeSerializer:
    content_type = PIPE_CONTENT_TYPE

    def dumps(self, document: object) -> str:
        if not isinstance(document, dict):
            raise TypeError('document must be a dict')
        pairs = [
            f'{name}={field_value}' for name, field_value in document.items()
        ]
        return '|'.join(pairs)

    def loads(self, body: str) -> dict:
        parsed: dict[str, str] = {}
        for pair in body.split('|'):
            name, field_value = pair.split('=', maxsplit=1)
            parsed[name] = field_value
        return parsed


class Echo(RpcOperation):
    path = '/echo'
    serializer = DataclassJsonSerializer(schema=EchoDoc)


class TypedEcho(RpcOperation):
    path = '/echo'
    serializer = TypedDictJsonSerializer(schema=EchoTyped)


class PipeTemplate(RpcOperation):
    serializer = PipeSerializer()


class PipedEcho(PipeTemplate):
    path = '/pipe'


class DictEcho(RpcOperation):
    path = '/echo'


class SerializerTests(unittest.TestCase):
    def test_dataclass_roundtrip(self) -> None:
        http_transport = RecordingHttpTransport(
            response='{"text": "pong"}',
        )
        echo = Echo(
            client=Client(
                http_transport=http_transport,
                base_url=EXAMPLE_API,
            ),
        )

        reply = echo(text='ping')

        self.assertEqual(reply, EchoDoc(text='pong'))
        self.assertEqual(http_transport.body, '{"text": "ping"}')
        self.assertEqual(
            http_transport.headers['Content-Type'],
            'application/json',
        )

    def test_typed_dict_roundtrip(self) -> None:
        http_transport = RecordingHttpTransport(
            response='{"text": "pong"}',
        )
        echo = TypedEcho(
            client=Client(
                http_transport=http_transport,
                base_url=EXAMPLE_API,
            ),
        )

        reply = echo(text='ping')

        self.assertEqual(reply, {'text': 'pong'})
        self.assertEqual(http_transport.body, '{"text": "ping"}')
        self.assertEqual(
            http_transport.headers['Content-Type'],
            'application/json',
        )

    def test_custom_serializer_on_template(self) -> None:
        http_transport = RecordingHttpTransport(response='text=pong')
        echo = PipedEcho(
            client=Client(
                http_transport=http_transport,
                base_url=EXAMPLE_API,
            ),
        )

        reply = echo(text='ping')

        self.assertEqual(reply, {'text': 'pong'})
        self.assertEqual(http_transport.body, 'text=ping')
        self.assertEqual(
            http_transport.headers['Content-Type'],
            PIPE_CONTENT_TYPE,
        )

    def test_dict_default_rejects_set(self) -> None:
        echo = DictEcho(
            client=Client(
                http_transport=RecordingHttpTransport(response='{}'),
                base_url=EXAMPLE_API,
            ),
        )

        try:
            echo(tags={1, 2})
        except TypeError:
            return
        self.fail('TypeError expected')

    def test_default_serializer_is_dict_json(self) -> None:
        self.assertIsInstance(
            DictEcho.serializer,
            DictJsonSerializer,
        )


if __name__ == '__main__':
    unittest.main()
