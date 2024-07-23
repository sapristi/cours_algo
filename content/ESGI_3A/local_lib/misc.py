from IPython.core.display import HTML

# import micropip
# await micropip.install("matplotlib")

import matplotlib.pyplot as plt


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


def affiche_valeurs(titre: str = None, ylabel="Temps d'exécution (s)", **kwargs: list[tuple[int, int]]):
    """Affiche les valeurs passées en argument"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 3))
    for name, values in kwargs.items():
        xs = [value[0] for value in values]
        ys = [value[1] for value in values]
        ax.plot(xs, ys, "o-", label=name)
    fig.legend()
    ax.grid()
    ax.set_xlabel("Taille de l'entrée")
    ax.set_ylabel("Temps d'exécution (s)")
    if titre is not None:
        ax.set_title(titre)