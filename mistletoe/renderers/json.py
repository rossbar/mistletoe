"""
Abstract syntax tree renderer for mistletoe.
"""

import json
from mistletoe.renderers.base import BaseRenderer


class JsonRenderer(BaseRenderer):
    def render(self, token):
        """
        Returns the JSON string representation of the AST.

        Overrides super().render. Delegates the logic to ast_to_json.
        """
        return json.dumps(ast_to_json(token), indent=2) + "\n"

    def __getattr__(self, name):
        return lambda token: ""


def ast_to_json(token):
    """
    Recursively unrolls token attributes into dictionaries (token.children
    into lists).

    Returns:
        a dictionary of token's attributes.
    """
    node = {}
    # Python 3.6 uses [ordered dicts] [1].
    # Put in 'type' entry first to make the final tree format somewhat
    # similar to [MDAST] [2].
    #
    #   [1]: https://docs.python.org/3/whatsnew/3.6.html
    #   [2]: https://github.com/syntax-tree/mdast
    node["type"] = token.__class__.__name__
    node.update(token.__dict__)
    if "header" in node:
        node["header"] = ast_to_json(node["header"])
    if "children" in node:
        node["children"] = [ast_to_json(child) for child in node["children"]]
    return node
