"""Сериализаторы тела: dict по умолчанию и dataclass явно."""

import json
from dataclasses import asdict
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


def _schema_fields(document: object) -> dict[str, object]:
    """
    Поля документа как `dict` со строковыми ключами.

    Иначе `object` нельзя раскрыть через `**` в конструктор
    schema.
    """
    if not isinstance(document, dict):
        raise TypeError('document must be a dict')
    fields: dict[str, object] = {}
    for name, field_value in document.items():
        if not isinstance(name, str):
            raise TypeError('document keys must be strings')
        fields[name] = field_value
    return fields


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
        return json.dumps(
            asdict(self.schema(**_schema_fields(document=document))),
        )

    def loads(self, body: str) -> object:
        return self.schema(
            **_schema_fields(document=json.loads(body)),
        )
