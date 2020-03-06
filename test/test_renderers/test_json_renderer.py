from mistletoe import Document
from mistletoe.renderers.json import ast_to_json


def test_basic(data_regression):
    doc = Document(["# heading 1\n", "\n", "hello\n", "world\n"])
    output = ast_to_json(doc)
    data_regression.check(output)


def test_link_references(data_regression):
    doc = Document(["[bar][baz]\n", "\n", "[baz]: spam\n"])
    output = ast_to_json(doc)
    data_regression.check(output)
