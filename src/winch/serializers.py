"""Сериализаторы тела: dict по умолчанию и dataclass явно."""

import json
from dataclasses import asdict, is_dataclass
from typing import Protocol


JSON_CONTENT_TYPE = 'application/json'


class Serializer(Protocol):
    """Контракт: объект ↔ строка тела и Content-Type."""

    content_type: str

    def dumps(self, document: object) -> str:
        """Сериализовать документ в строку тела."""
        ...

    def loads(self, body: str) -> object:
        """Прочитать документ из строки тела."""
        ...


class DictJsonSerializer:
    """Дефолт базы: dict через stdlib json."""

    content_type = JSON_CONTENT_TYPE

    def dumps(self, document: object) -> str:
        return json.dumps(document)

    def loads(self, body: str) -> dict:
        return json.loads(body)


class DataclassJsonSerializer:
    """Явный сериализатор dataclass через stdlib json."""

    content_type = JSON_CONTENT_TYPE

    def __init__(self, schema: type) -> None:
        self.schema = schema

    def dumps(self, document: object) -> str:
        dataclass_document = document
        if not is_dataclass(dataclass_document) or isinstance(
            dataclass_document,
            type,
        ):
            dataclass_document = self.schema(**document)
        return json.dumps(asdict(dataclass_document))

    def loads(self, body: str) -> object:
        return self.schema(**json.loads(body))
