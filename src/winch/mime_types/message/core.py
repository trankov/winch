from .types import MessageMediaType


class bhttp(MessageMediaType):
    name = 'bhttp'
    mime_subtype = 'bhttp'


class cpim(MessageMediaType):
    name = 'CPIM'
    mime_subtype = 'CPIM'


class delivery_status(MessageMediaType):
    name = 'delivery-status'
    mime_subtype = 'delivery-status'


class disposition_notification(MessageMediaType):
    name = 'disposition-notification'
    mime_subtype = 'disposition-notification'


class example(MessageMediaType):
    name = 'example'
    mime_subtype = 'example'


class external_body(MessageMediaType):
    name = 'external-body'
    mime_subtype = 'external-body'


class feedback_report(MessageMediaType):
    name = 'feedback-report'
    mime_subtype = 'feedback-report'


class global_(MessageMediaType):
    name = 'global'
    mime_subtype = 'global'


class global_delivery_status(MessageMediaType):
    name = 'global-delivery-status'
    mime_subtype = 'global-delivery-status'


class global_disposition_notification(MessageMediaType):
    name = 'global-disposition-notification'
    mime_subtype = 'global-disposition-notification'


class global_headers(MessageMediaType):
    name = 'global-headers'
    mime_subtype = 'global-headers'


class http(MessageMediaType):
    name = 'http'
    mime_subtype = 'http'


class imdn_xml(MessageMediaType):
    name = 'imdn+xml'
    mime_subtype = 'imdn+xml'


class mls(MessageMediaType):
    name = 'mls'
    mime_subtype = 'mls'


class ohttp_req(MessageMediaType):
    name = 'ohttp-req'
    mime_subtype = 'ohttp-req'


class ohttp_res(MessageMediaType):
    name = 'ohttp-res'
    mime_subtype = 'ohttp-res'


class partial(MessageMediaType):
    name = 'partial'
    mime_subtype = 'partial'


class rfc822(MessageMediaType):
    name = 'rfc822'
    mime_subtype = 'rfc822'


class sip(MessageMediaType):
    name = 'sip'
    mime_subtype = 'sip'


class sipfrag(MessageMediaType):
    name = 'sipfrag'
    mime_subtype = 'sipfrag'


class tracking_status(MessageMediaType):
    name = 'tracking-status'
    mime_subtype = 'tracking-status'


class vnd_wfa_wsc(MessageMediaType):
    name = 'vnd.wfa.wsc'
    mime_subtype = 'vnd.wfa.wsc'
