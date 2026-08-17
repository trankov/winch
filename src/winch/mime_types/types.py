class IanaMediaType:
    __slots__ = (
        'name',
        'mime_type',
        'mime_subtype',
        'parameters',
    )
    name: str
    mime_type: str
    mime_subtype: str

    def __init__(self, **parameters: str) -> None:
        self.parameters = parameters or {}

    def _get_parameters(self) -> str:
        return ';'.join(
            f'{name}={value}' for name, value in self.parameters.items()
        )

    def __str__(self) -> str:
        _template = f'{self.mime_type}/{self.mime_subtype}'
        if _parameters := self._get_parameters():
            return f'{_template};{_parameters}'
        return _template

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__} [{self}]>'
        )
