from .types import MultipartMediaType


class alternative(MultipartMediaType):
    name = 'alternative'
    mime_subtype = 'alternative'


class appledouble(MultipartMediaType):
    name = 'appledouble'
    mime_subtype = 'appledouble'


class byteranges(MultipartMediaType):
    name = 'byteranges'
    mime_subtype = 'byteranges'


class digest(MultipartMediaType):
    name = 'digest'
    mime_subtype = 'digest'


class encrypted(MultipartMediaType):
    name = 'encrypted'
    mime_subtype = 'encrypted'


class example(MultipartMediaType):
    name = 'example'
    mime_subtype = 'example'


class form_data(MultipartMediaType):
    name = 'form-data'
    mime_subtype = 'form-data'


class header_set(MultipartMediaType):
    name = 'header-set'
    mime_subtype = 'header-set'


class mixed(MultipartMediaType):
    name = 'mixed'
    mime_subtype = 'mixed'


class multilingual(MultipartMediaType):
    name = 'multilingual'
    mime_subtype = 'multilingual'


class parallel(MultipartMediaType):
    name = 'parallel'
    mime_subtype = 'parallel'


class related(MultipartMediaType):
    name = 'related'
    mime_subtype = 'related'


class report(MultipartMediaType):
    name = 'report'
    mime_subtype = 'report'


class signed(MultipartMediaType):
    name = 'signed'
    mime_subtype = 'signed'


class vnd_bint_med_plus(MultipartMediaType):
    name = 'vnd.bint.med-plus'
    mime_subtype = 'vnd.bint.med-plus'


class voice_message(MultipartMediaType):
    name = 'voice-message'
    mime_subtype = 'voice-message'


class x_mixed_replace(MultipartMediaType):
    name = 'x-mixed-replace'
    mime_subtype = 'x-mixed-replace'
