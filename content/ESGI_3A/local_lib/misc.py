from IPython.core.display import HTML

def custom_markdown_style():
    css = HTML("""
    <style>
    .jp-Cell.jp-MarkdownCell {
        max-width: 900px;
        margin-left: 100px;
        box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
        padding-bottom: 20px;
    }
    .jp-MarkdownOutput > :not(h1, h2, h3, table) {
      margin-left: 50px;
      margin-right: 50px;
    }
    </style>""")
    display(css)