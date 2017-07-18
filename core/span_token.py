import re
import html
import core.span_tokenizer as tokenizer

__all__ = ['EscapeSequence', 'Emphasis', 'Strong', 'InlineCode',
           'Strikethrough', 'Image', 'Link']

def tokenize_inner(content):
    token_types = [ globals()[key] for key in __all__ ]
    fallback_token = RawText
    lt = tokenizer.SpanTokenizer(content, token_types, fallback_token)
    return lt.get_tokens()

class SpanToken(object):
    def __init__(self, content):
        self.children = tokenize_inner(content)

class Strong(SpanToken):
    pattern = re.compile(r"\*\*(.+?)\*\*(?!\*)|__(.+)__(?!_)")
    def __init__(self, raw):
        super().__init__(raw)

class Emphasis(SpanToken):
    pattern = re.compile(r"\*((?:\*\*|[^\*])+?)\*(?!\*)|_((?:__|[^_])+?)_")
    def __init__(self, raw):
        super().__init__(raw)

class InlineCode(SpanToken):
    pattern = re.compile(r"`(.+?)`")
    def __init__(self, raw):
        super().__init__(raw)

class Strikethrough(SpanToken):
    pattern = re.compile(r"~~(.+)~~")
    def __init__(self, raw):
        super().__init__(raw)

class Image(SpanToken):
    pattern = re.compile(r"(\!\[(.+?)\]\((.+?)\))")
    def __init__(self, raw):
        self.alt = raw[2:raw.index(']')]
        target = raw[raw.index('(')+1:-1]
        if target.find('"') != -1:
            self.target = target[:target.index(' "')]
            self.title = target[target.index(' "')+2:-1]
        else:
            self.target = target
            self.title = ''

class Link(SpanToken):
    pattern = re.compile(r"(\[((?:!\[(.+?)\]\((.+?)\))|(?:.+?))\]\((.+?)\))")
    def __init__(self, raw):
        split_index = len(raw) - raw[::-1].index(']') - 1
        super().__init__(raw[1:split_index])
        self.target = raw[split_index+2:-1]

class EscapeSequence(SpanToken):
    pattern = re.compile(r"\\([\*\(\)\[\]\~])")
    def __init__(self, raw):
        self.content = raw

class RawText(SpanToken):
    def __init__(self, content):
        self.content = content