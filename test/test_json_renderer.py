import unittest
from mistletoe import Document
from mistletoe.renderers.json import ast_to_json


class TestJSONRenderer(unittest.TestCase):
    def test(self):
        self.maxDiff = None
        d = Document(["# heading 1\n", "\n", "hello\n", "world\n"])
        output = ast_to_json(d)
        target = {
            "type": "Document",
            "footnotes": {},
            "children": [
                {
                    "type": "Heading",
                    "level": 1,
                    "children": [{"type": "RawText", "content": "heading 1"}],
                },
                {
                    "type": "Paragraph",
                    "children": [
                        {"type": "RawText", "content": "hello"},
                        {"type": "LineBreak", "soft": True, "content": ""},
                        {"type": "RawText", "content": "world"},
                    ],
                },
            ],
        }
        self.assertEqual(output, target)

    def test_footnotes(self):
        self.maxDiff = None
        d = Document(["[bar][baz]\n", "\n", "[baz]: spam\n"])
        target = {
            "type": "Document",
            "footnotes": {"baz": ("spam", "")},
            "children": [
                {
                    "type": "Paragraph",
                    "children": [
                        {
                            "type": "Link",
                            "target": "spam",
                            "title": "",
                            "children": [{"type": "RawText", "content": "bar"}],
                        }
                    ],
                }
            ],
        }
        output = ast_to_json(d)
        self.assertEqual(output, target)
