"""
WebDAV methods, based on IANA assignments.
The same as http.HTTPMethod, but for WebDAV.
"""

from enum import StrEnum, _simple_enum


@_simple_enum(StrEnum)
class WebDavMethod:
    """
    Web Distributed Authoring and Versioning (WebDAV) methods
    and descriptions

    https://www.iana.org/assignments/http-methods/http-methods.xhtml
    """

    def __new__(cls, value, description):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}.{self._name_}>"

    ACL = ('ACL', 'Modifies the access control list of a resource')
    BASELINE_CONTROL = (
        'BASELINE-CONTROL',
        'Associates a baseline with a version-controlled collection',
    )
    BIND = (
        'BIND',
        'Creates a new binding from a collection to an existing resource',
    )
    CHECKIN = (
        'CHECKIN',
        'Creates a new version of a checked-out resource and ends '
        'the checkout',
    )
    CHECKOUT = (
        'CHECKOUT',
        'Places a version-controlled resource in the checked-out state'
        ' for editing',
    )
    CONNECT = (
        'CONNECT',
        'Establishes a tunnel to the server identified by the target'
        ' resource',
    )
    COPY = (
        'COPY',
        'Creates a duplicate of the source resource at a destination URI',
    )
    DELETE = (
        'DELETE',
        'Removes the target resource and its associated mappings',
    )
    GET = (
        'GET',
        'Transfers a current representation of the target resource',
    )
    HEAD = (
        'HEAD',
        'Identical to GET but returns only the headers for diagnostics',
    )
    LABEL = (
        'LABEL',
        'Applies, modifies, or removes a label for a version-controlled'
        ' resource',
    )
    LINK = (
        'LINK',
        'Establishes one or more relationships between the requested'
        ' resource and other resources',
    )
    LOCK = (
        'LOCK',
        'Requests a lock to prevent conflicting changes to a resource',
    )
    MERGE = (
        'MERGE',
        'Combines changes from different versions into a checked-out resource',
    )
    MKACTIVITY = (
        'MKACTIVITY',
        'Creates a new activity resource to collect related versioning'
        ' operations',
    )
    MKCALENDAR = (
        'MKCALENDAR',
        'Creates a new calendar collection resource (CalDAV)',
    )
    MKCOL = (
        'MKCOL',
        'Creates a new collection resource at the request URI',
    )
    MKREDIRECTREF = (
        'MKREDIRECTREF',
        'Creates a redirect reference resource that forwards future requests',
    )
    MKWORKSPACE = (
        'MKWORKSPACE',
        'Creates a new workspace resource for grouping version-controlled'
        ' resources',
    )
    MOVE = (
        'MOVE',
        'Moves a resource to a new URI, removing the source on success',
    )
    OPTIONS = (
        'OPTIONS',
        'Describes the communication options available for the target'
        ' resource',
    )
    ORDERPATCH = (
        'ORDERPATCH',
        'Changes the ordering of members within an ordered collection',
    )
    PATCH = (
        'PATCH',
        'Applies partial modifications to the target resource',
    )
    POST = (
        'POST',
        'Submits data to be processed according to the target resource'
        ' semantics',
    )
    PRI = (
        'PRI',
        'Reserved method used in the HTTP/2 connection preface',
    )
    PROPFIND = (
        'PROPFIND',
        'Retrieves properties for a resource and can enumerate collection'
        ' members',
    )
    PROPPATCH = (
        'PROPPATCH',
        'Sets or removes multiple properties on a resource in a single'
        ' request',
    )
    PUT = (
        'PUT',
        'Creates or replaces the target resource with the request payload',
    )
    REBIND = (
        'REBIND',
        'Moves an existing binding to a new parent without copying the'
        ' resource',
    )
    REPORT = (
        'REPORT',
        'Returns information based on a server-defined report type for'
        ' DAV resources',
    )
    SEARCH = (
        'SEARCH',
        'Executes a server-side search query against a WebDAV resource',
    )
    TRACE = (
        'TRACE',
        'Provides a message loop-back test along the request path '
        'for diagnostics',
    )
    UNBIND = (
        'UNBIND',
        'Removes a binding from a collection to a resource',
    )
    UNCHECKOUT = (
        'UNCHECKOUT',
        'Cancels a checkout and discards uncommitted changes',
    )
    UNLINK = (
        'UNLINK',
        'Removes link relationships previously established with LINK',
    )
    UNLOCK = (
        'UNLOCK',
        'Removes a lock from the target resource',
    )
    UPDATE = (
        'UPDATE',
        'Applies a selected version to a version-controlled resource',
    )
    UPDATEREDIRECTREF = (
        'UPDATEREDIRECTREF',
        'Changes the target URI of an existing redirect reference resource',
    )
    VERSION_CONTROL = (
        'VERSION-CONTROL',
        'Places an existing resource under version control',
    )


__all__ = ('WebDavMethod',)
