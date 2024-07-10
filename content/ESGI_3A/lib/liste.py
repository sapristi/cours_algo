from pydantic import BaseModel
from typing import Union

class List(BaseModel):
    """
    Implémentation d'une liste chaînée en python.
    
    Note: on considère que si value est None, alors la liste est vide
    (dans ce cas, next est sensé valoir None aussi).
    Si value n'est pas None, next ne doit pas valoir None.
    """
    value: str | None
    next: Union["List", None] = None

    def __init__(self, value=None, next=None):
        if value is None:
            if next is not None:
                raise ValueError("Cannot have empty list with next part")
            super().__init__(value=None, next=None)
    
        else:
            if next is None:
                next = EMPTY    
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
        if not isinstance(other, List):
            return False

        if self.is_empty() or other.is_empty():
            return self.is_empty() == other.is_empty()
        if self.value != other.value:
            return False
        return self.next == other.next

    def __radd__(self, value):
        """Permet d'utiliser l'opérateur + pour construire une liste"""
        if isinstance(value, List):
            raise NotImplementedError
        res = List(value, self)
        return res

class EmptyList(List):
    """Classe qui représente une liste vide. Les instances ne peuvent pas être modifiées."""
    def __init__(self):
        super().__init__(value=None, next=None)
    def __setattr__(self, key, value):
        if hasattr(self, "value"):
            raise Exception("Object is frozen")
        super().__setattr__(key, value)

EMPTY = EmptyList()