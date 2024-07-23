import pydantic
from typing import Union

class BaseModel(pydantic.BaseModel):
    class Config:
        extra="forbid"

def not_implemented(cls, *args, **kwargs):
    raise NotImplementedError

class RemoveMethods(type):
    def __new__(mcls, name, bases, attrs):
        cls = super().__new__(mcls, name, bases, attrs)
        builtins_to_deactivate = {"__add__","__radd__", "append", "extend", "insert", "pop", "reverse", "sort", "__contains__", "remove", "__delitem__", "__iter__", "__len__" }
        for method in builtins_to_deactivate  - attrs.keys():
            setattr(cls, method, not_implemented)
        return cls



class Etagère(list[str], metaclass=RemoveMethods):
    """Classe pour une étagère: """
    def __init__(self, capacité: int):
        super().__init__([None] * capacité)
        self.capacité = capacité
        
    def _repr_html_(self):
        """Sert à afficher l'objet dans un environnement jupyter"""
        def row(values):
            return "".join(f"<td>{value}</td>" for value in values)
        return f"""
        <style> table, th, td {{ border: 1px solid black !important; }} </style>
        <table>
            <tr><th>indice</th>{row(range(self.capacité))}</tr>
            <tr><th>valeur</th>{row(self[i] for i in range(self.capacité))}</tr>
        </table>
        """


class Liste(BaseModel):
    """
    Implémentation d'une liste chaînée en python.
    
    Note: on considère que si value est None, alors la liste est vide
    (dans ce cas, next est sensé valoir None aussi).
    Si value n'est pas None, next ne doit pas valoir None.
    """
    value: str | None
    next: Union["Liste", None] = None

    def __init__(self, value=None, next=None):
        if value is None:
            if next is not None:
                raise ValueError("Cannot have empty list with next part")
            super().__init__(value=None, next=None)
    
        else:
            if next is None:
                next = VIDE    
            super().__init__(value=value, next=next)

    def is_empty(self):
        return self.value is None

    def _repr_html_(self):
        """Affichage custom dans Jupyter"""
        if self.is_empty():
            return "■"
        return str(self.value) + " ⟶ " + self.next._repr_html_()

    def __eq__(self, other):
        """Test d'égalité"""
        if not isinstance(other, Liste):
            return False

        if self.is_empty() or other.is_empty():
            return self.is_empty() == other.is_empty()
        if self.value != other.value:
            return False
        return self.next == other.next

    def __radd__(self, value):
        """Permet d'utiliser l'opérateur + pour construire une liste"""
        if isinstance(value, Liste):
            raise NotImplementedError
        res = Liste(value, self)
        return res

class ListeVide(Liste):
    """Classe qui représente une liste vide. Les instances ne peuvent pas être modifiées."""
    def __init__(self):
        super().__init__(value=None, next=None)
    def __setattr__(self, key, value):
        if hasattr(self, "value"):
            raise Exception("Object is frozen")
        super().__setattr__(key, value)

ListeVide.update_forward_refs()

VIDE = ListeVide()


class BTree(BaseModel):
    left: Union["BTree", None] = None
    right: Union["BTree", None] = None
    value: int | str


    def _repr_aux(self) -> tuple[int, list[str]]:
        lines = []
        if self.left:
            left_root_index, lines_left = self.left._repr_aux()
            for i, line in enumerate(lines_left):
                if i < left_root_index:
                    lines.append("   " + line)
                elif i == left_root_index:
                    lines.append("╭─╴" + line)
                else:
                    lines.append("│  " + line)
            
        root_index = len(lines)
        lines.append(str(self.value))
        
        if self.right:
            right_root_index, lines_right = self.right._repr_aux()
            for i, line in enumerate(lines_right):
                if i < right_root_index:
                    lines.append("│  " + line)
                elif i == right_root_index:
                    lines.append("╰─╴" + line)
                else:
                    lines.append("   " + line)
    
        return root_index, lines

    def __repr__(self):
        root_index, lines = self._repr_aux()
        lines_res = []
        for i, line in enumerate(lines):
            if i == root_index:
                lines_res.append("──" + line)
            else:
                lines_res.append("  " + line)
        return "\n".join(lines_res)
BTree.update_forward_refs()