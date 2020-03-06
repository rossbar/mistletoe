from mistletoe import Document, HTMLRenderer, __version__

INCLUDE = {"README.md": "index.html", "CONTRIBUTING.md": "contributing.html"}

METADATA = """
<head>
  <title>mistletoe{}</title>
  <meta charset="UTF-8" />
  <meta name="description" content="A fast, extensible Markdown parser in Python." />
  <meta name="keywords" content="Markdown,Python,LaTeX,HTML" />
  <meta name="author" content="Mi Yu" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" href="style.css" type="text/css" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/styles/github.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/highlight.min.js"></script>
  <script>hljs.initHighlightingOnLoad();</script>
</head>
"""  # noqa: E501


class DocRenderer(HTMLRenderer):
    def render_link(self, token):
        return super().render_link(self._replace_link(token))

    def render_document(self, token, name="README.md"):
        pattern = "<html>{}<body>{}</body></html>"
        self.link_definitions.update(token.link_definitions)
        for filename, new_link in getattr(self, "files", {}).items():
            for k, v in self.link_definitions.items():
                if v == filename:
                    self.link_definitions[k] = new_link
        subtitle = " | {}".format(
            "version " + __version__
            if name == "README.md"
            else name.split(".")[0].lower()
        )
        return pattern.format(METADATA.format(subtitle), self.render_inner(token))

    def _replace_link(self, token):
        token.target = getattr(self, "files", {}).get(token.target, token.target)
        return token


def build(files=None):
    files = files or INCLUDE
    for f in files:
        with open(f, "r") as fin:
            rendered_file = "docs/" + files[f]
            with open(rendered_file, "w+") as fout:
                with DocRenderer() as renderer:
                    renderer.files = files
                    print(renderer.render_document(Document.read(fin), f), file=fout)
