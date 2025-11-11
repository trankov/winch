import unittest
from enum import StrEnum

from winch.methods import WebDavMethod


class WebDavMethodTests(unittest.TestCase):
    def test_member_value_and_description(self) -> None:
        self.assertEqual(WebDavMethod.PROPFIND, 'PROPFIND')
        self.assertEqual(
            WebDavMethod.PROPFIND.description,
            'Retrieves properties for a resource and can enumerate collection'
            ' members',
        )

    def test_members_are_str_enum_instances(self) -> None:
        member = WebDavMethod.COPY

        self.assertIsInstance(member, StrEnum)
        self.assertIsInstance(member, WebDavMethod)
        self.assertEqual(
            member.description,
            'Creates a duplicate of the source resource at a destination URI',
        )

    def test_repr_uses_class_and_member_name(self) -> None:
        self.assertEqual(repr(WebDavMethod.LOCK), '<WebDavMethod.LOCK>')

    def test_iteration_covers_all_registered_methods(self) -> None:
        expected_values = {
            'ACL',
            'BASELINE-CONTROL',
            'BIND',
            'CHECKIN',
            'CHECKOUT',
            'CONNECT',
            'COPY',
            'DELETE',
            'GET',
            'HEAD',
            'LABEL',
            'LINK',
            'LOCK',
            'MERGE',
            'MKACTIVITY',
            'MKCALENDAR',
            'MKCOL',
            'MKREDIRECTREF',
            'MKWORKSPACE',
            'MOVE',
            'OPTIONS',
            'ORDERPATCH',
            'PATCH',
            'POST',
            'PRI',
            'PROPFIND',
            'PROPPATCH',
            'PUT',
            'REBIND',
            'REPORT',
            'SEARCH',
            'TRACE',
            'UNBIND',
            'UNCHECKOUT',
            'UNLINK',
            'UNLOCK',
            'UPDATE',
            'UPDATEREDIRECTREF',
            'VERSION-CONTROL',
        }

        self.assertSetEqual(
            {member.value for member in WebDavMethod}, expected_values
        )

    def test_lookup_by_value_returns_enum_member(self) -> None:
        self.assertIs(WebDavMethod('LOCK'), WebDavMethod.LOCK)


if __name__ == '__main__':
    unittest.main()
