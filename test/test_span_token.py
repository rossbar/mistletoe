import pytest

from mistletoe.span_tokenizer import tokenize_span
from mistletoe.span_tokens import HTMLSpan
from mistletoe.base_elements import serialize_tokens
from mistletoe.parse_context import get_parse_context


@pytest.mark.parametrize(
    "name,source",
    [
        ("star", "**some text**"),
        ("underline", "__some text__"),
        ("multi", "**one** **two**"),
    ],
)
def test_strong(name, source, data_regression):
    data_regression.check(
        serialize_tokens(tokenize_span(source), as_dict=True),
        basename=f"test_strong_{name}",
    )


@pytest.mark.parametrize(
    "name,source",
    [("star", "*some text*"), ("underline", "_some text_"), ("multi", "*one* *two*")],
)
def test_emphasis(name, source, data_regression):
    data_regression.check(
        serialize_tokens(tokenize_span(source), as_dict=True),
        basename=f"test_emphasis_{name}",
    )


@pytest.mark.parametrize(
    "name,source", [("basic", "`some text`"), ("multi", "`one` `two`")]
)
def test_inline_code(name, source, data_regression):
    data_regression.check(
        serialize_tokens(tokenize_span(source), as_dict=True),
        basename=f"test_inline_code_{name}",
    )


@pytest.mark.parametrize(
    "name,source", [("basic", "~~some text~~"), ("multi", "~~one~~ ~~two~~")]
)
def test_strikethrough(name, source, data_regression):
    data_regression.check(
        serialize_tokens(tokenize_span(source), as_dict=True),
        basename=f"test_strikethrough_{name}",
    )


@pytest.mark.parametrize(
    "name,source",
    [
        ("basic", "[name 1](target1)"),
        ("multi", "[n1](t1) & [n2](t2)"),
        ("children", "[![alt](src)](target)"),
    ],
)
def test_link(name, source, data_regression):
    data_regression.check(
        serialize_tokens(tokenize_span(source), as_dict=True),
        basename=f"test_link_{name}",
    )


@pytest.mark.parametrize("name,source", [("basic", "<ftp://foo.com>")])
def test_auto_link(name, source, data_regression):
    data_regression.check(
        serialize_tokens(tokenize_span(source), as_dict=True),
        basename=f"test_auto_link_{name}",
    )


@pytest.mark.parametrize(
    "name,source",
    [
        ("basic", "![alt](link)"),
        ("with_title", '![alt](link "title")'),
        ("no_alt", "![](link)"),
    ],
)
def test_image(name, source, data_regression):
    data_regression.check(
        serialize_tokens(tokenize_span(source), as_dict=True),
        basename=f"test_image_{name}",
    )


@pytest.mark.parametrize(
    "name,source", [("single_star", "\\*"), ("emphasis", "some \\*text*")]
)
def test_escape_sequence(name, source, data_regression):
    data_regression.check(
        serialize_tokens(tokenize_span(source), as_dict=True),
        basename=f"test_escape_sequence_{name}",
    )


@pytest.mark.parametrize("name,source", [("basic", "some text")])
def test_raw_text(name, source, data_regression):
    data_regression.check(
        serialize_tokens(tokenize_span(source), as_dict=True),
        basename=f"test_raw_text_{name}",
    )


@pytest.mark.parametrize("name,source", [("basic", "  \n")])
def test_line_break(name, source, data_regression):
    data_regression.check(
        serialize_tokens(tokenize_span(source), as_dict=True),
        basename=f"test_line_break_{name}",
    )


@pytest.mark.parametrize("name,source", [("basic", "<p>some text</p>")])
def test_html_span(name, source, data_regression):
    get_parse_context().span_tokens.insert(1, HTMLSpan)
    data_regression.check(
        serialize_tokens(tokenize_span(source), as_dict=True),
        basename=f"test_html_span_{name}",
    )


@pytest.mark.parametrize(
    "name,source",
    [
        ("emph_in_strong", "**with some *emphasis* text**"),
        ("strong_in_emph", "*with some **strong** text*"),
        ("star_underline", "*__some text__*"),
        ("underline_star", "__*some text*__"),
        ("emph_in_link", "[*some text*](link)"),
        ("link_in_emph", "*[*some text*](link)*"),
        ("star_in_inline_code", "`*a*`"),
        ("underscore_in_inline_code", "`_a_`"),
        ("inline_code_in_star", "*`a`*"),
        ("inline_code_in_underscore", "_`a`_"),
    ],
)
def test_nested(name, source, data_regression):
    data_regression.check(
        serialize_tokens(tokenize_span(source), as_dict=True),
        basename=f"test_nested_{name}",
    )
