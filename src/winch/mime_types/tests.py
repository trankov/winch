import unittest

from . import text, video
from .text.types import TextMediaType
from .types import IanaMediaType


class IanaMediaTypeTests(unittest.TestCase):
    def test_str_without_parameters(self) -> None:
        media = text.plain()

        self.assertEqual(media.parameters, {})
        self.assertEqual(str(media), 'text/plain')
        self.assertEqual(media._get_parameters(), '')

    def test_str_with_parameters(self) -> None:
        media = text.html(charset='utf-8', profile='strict')

        self.assertEqual(
            media.parameters,
            {'charset': 'utf-8', 'profile': 'strict'},
        )
        self.assertEqual(
            media._get_parameters(),
            'charset=utf-8;profile=strict',
        )
        self.assertEqual(str(media), 'text/html;charset=utf-8;profile=strict')

    def test_repr_uses_class_name(self) -> None:
        media = text.html(charset='utf-8')

        self.assertEqual(
            repr(media),
            '<html [text/html;charset=utf-8]>',
        )


class MediaTypeHierarchyTests(unittest.TestCase):
    def test_text_media_type_inherits_base(self) -> None:
        media = text.plain()

        self.assertIsInstance(media, TextMediaType)
        self.assertIsInstance(media, IanaMediaType)
        self.assertEqual(media.mime_type, 'text')
        self.assertEqual(media.mime_subtype, 'plain')

    def test_video_media_type_inherits_base(self) -> None:
        media = video.mp4()

        self.assertIsInstance(media, IanaMediaType)
        self.assertEqual(media.mime_type, 'video')
        self.assertEqual(media.mime_subtype, 'mp4')
        self.assertEqual(str(media), 'video/mp4')


if __name__ == '__main__':
    unittest.main()
