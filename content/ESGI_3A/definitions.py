import sys
from typing import Iterable
from gelidum import freeze

import matplotlib.pyplot as plt

def not_implemented(cls, *args, **kwargs):
    raise NotImplementedError

class RemoveMethods(type):
    def __new__(mcls, name, bases, attrs):
        cls = super().__new__(mcls, name, bases, attrs)
        for method in ("__add__","__radd__", "append", "extend", "insert", "pop", "reverse", "sort", "__contains__", "remove", "__delitem__", "__iter__"):
            setattr(cls, method, not_implemented)
        return cls


class Étagère(list[str], metaclass=RemoveMethods):
    """Classe de base pour un tableau"""
    def __init__(self, capacité: int):
        super().__init__([None] * capacité)
        self.capacité = capacité
        
    def _repr_html_(self):
        def row(values):
            return "".join(f"<td>{value}</td>" for value in values)
        return f"""
        <style> table, th, td {{ border: 1px solid black !important; }} </style>
        <table>
            <tr><th>indice</th>{row(range(len(self)))}</tr>
            <tr><th>valeur</th>{row(self[i] for i in range(len(self)))}</tr>
        </table>
        """
