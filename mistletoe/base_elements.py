from collections import namedtuple
from typing import List, Optional


WalkItem = namedtuple("WalkItem", ["node", "parent", "depth"])


class Token:
    """Base class of all mistletoe tokens."""

    def __getattr__(self, name):
        # ensure certain attributes are always available
        if name == "children":
            return None
        if name == "content":
            return ""

    @property
    def name(self):
        """Return the name of the element."""
        return type(self).__name__

    def __contains__(self, text: str):
        """Return is text is contained in the element or its ancestors."""
        if self.children is None:
            return text in self.content
        return any(text in child for child in self.children)

    def __repr__(self):
        """A base represent method, that can be overriden for more complex elements."""
        info = []
        if self.children is not None:
            info.append("children={}".format(len(self.children)))
        return "{}({})".format(self.name, ",".join(info))

    def walk(
        self,
        tokens: Optional[List[str]] = None,
        depth: Optional[int] = None,
        include_self: bool = False,
    ) -> WalkItem:
        """Traverse the syntax tree, recursively yielding children.

        :param elements: filter children by certain token names.
        :param depth: The depth to recurse into the tree.
        :param include_self: whether to first yield this element.

        :yield: A container for an element, its parent and depth

        """
        current_depth = 0
        if include_self:
            yield WalkItem(self, None, current_depth)
        next_children = [(self, c) for c in self.children or []]
        while next_children and (depth is None or current_depth > depth):
            current_depth += 1
            new_children = []
            for parent, child in next_children:
                if tokens is None or child.name in tokens:
                    yield WalkItem(child, parent, current_depth)
                new_children.extend([(child, c) for c in child.children or []])
            next_children = new_children


class BlockToken(Token):
    """Base class for block-level tokens. Recursively parse inner tokens.

    Naming conventions:

    * lines denotes a list of (possibly unparsed) input lines, and is
        commonly used as the argument name for constructors.

    * BlockToken.children is a list with all the inner tokens (thus if
        a token has children attribute, it is not a leaf node; if a token
        calls tokenize_span, it is the boundary between
        span-level tokens and block-level tokens);

    * BlockToken.start takes a line from the document as argument, and
        returns a boolean representing whether that line marks the start
        of the current token. Every subclass of BlockToken must define a
        start function (see block_tokenizer.tokenize).

    * BlockToken.read takes the rest of the lines in the document as an
        iterator (including the start line), and consumes all the lines
        that should be read into this token.

        Default to stop at an empty line.

        Note that BlockToken.read does not have to return a list of lines.
        Because the return value of this function will be directly
        passed into the token constructor, we can return any relevant
        parsing information, sometimes even ready-made tokens,
        into the constructor. See block_tokenizer.tokenize.

        If BlockToken.read returns None, the read result is ignored,
        but the token class is responsible for resetting the iterator
        to a previous state. See block_tokenizer.FileWrapper.anchor,
        block_tokenizer.FileWrapper.reset.

    """

    def __init__(self, lines, tokenize_func):
        self.children = tokenize_func(lines)

    @classmethod
    def start(cls, line: str):
        """Takes a line from the document as argument, and
        returns a boolean representing whether that line marks the start
        of the current token. Every subclass of BlockToken must define a
        start function (see `block_tokenizer.tokenize_main`).
        """
        raise NotImplementedError

    @classmethod
    def read(cls, lines):
        """takes the rest of the lines in the document as an
        iterator (including the start line), and consumes all the lines
        that should be read into this token.

        The default is to stop at an empty line.
        """
        line_buffer = [next(lines)]
        for line in lines:
            if line == "\n":
                break
            line_buffer.append(line)
        return line_buffer


class SpanToken(Token):
    """Base class for span-level tokens.

    - `pattern`: regex pattern to search for
    - To parse child tokens, `parse_inner` should be set to `True`.
    - `parse_group` corresponds to the match group in which child tokens might occur
    - `precedence`: Alter the relative order by which the span token is assessed.
    """

    pattern = None
    parse_inner = True
    parse_group = 1
    precedence = 5

    def __init__(self, match):
        if not self.parse_inner:
            self.content = match.group(self.parse_group)

    @classmethod
    def find(cls, string: str):
        """Find all tokens, matching a pattern in the given string"""
        if cls.pattern is not None:
            return cls.pattern.finditer(string)
        return []
