from mistletoe import Document
from mistletoe.renderers.json import ast_to_json, JsonRenderer
from mistletoe.latex_token import Math


def test_basic(data_regression):
    doc = Document(["# heading 1\n", "\n", "hello\n", "world\n"])
    output = ast_to_json(doc)
    data_regression.check(output)


def test_link_references(data_regression):
    doc = Document(["[bar][baz]\n", "\n", "[baz]: spam\n"])
    output = ast_to_json(doc)
    data_regression.check(output)


def test_extra_tokens():
    """Extra tokens should persist between multiple calls of the same renderer,
    but be reset if initiating a new renderer.
    """
    with JsonRenderer() as render:
        output = render.render(Document(["$b$"]), as_string=False)
    assert output == {
        "type": "Document",
        "link_definitions": {},
        "children": [
            {"type": "Paragraph", "children": [{"type": "RawText", "content": "$b$"}]}
        ],
    }
    renderer = JsonRenderer(Math)
    with renderer as render:
        output = render.render(Document(["$b$"]), as_string=False)
    assert output == {
        "type": "Document",
        "link_definitions": {},
        "children": [
            {"type": "Paragraph", "children": [{"type": "Math", "content": "$b$"}]}
        ],
    }
    with renderer as render:
        output = render.render(Document(["$b$"]), as_string=False)
    assert output == {
        "type": "Document",
        "link_definitions": {},
        "children": [
            {"type": "Paragraph", "children": [{"type": "Math", "content": "$b$"}]}
        ],
    }
    with JsonRenderer() as render:
        output = render.render(Document(["$b$"]), as_string=False)
    assert output == {
        "type": "Document",
        "link_definitions": {},
        "children": [
            {"type": "Paragraph", "children": [{"type": "RawText", "content": "$b$"}]}
        ],
    }
