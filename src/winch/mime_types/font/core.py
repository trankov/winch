from .types import FontMediaType


class collection(FontMediaType):
    name = 'collection'
    mime_subtype = 'collection'


class otf(FontMediaType):
    name = 'otf'
    mime_subtype = 'otf'


class sfnt(FontMediaType):
    name = 'sfnt'
    mime_subtype = 'sfnt'


class ttf(FontMediaType):
    name = 'ttf'
    mime_subtype = 'ttf'


class woff(FontMediaType):
    name = 'woff'
    mime_subtype = 'woff'


class woff2(FontMediaType):
    name = 'woff2'
    mime_subtype = 'woff2'
