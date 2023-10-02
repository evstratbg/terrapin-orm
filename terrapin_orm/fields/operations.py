from typing import Any
from abc import abstractmethod


class Operators:
    def __init__(self, column: str, value: Any):
        self.column = column
        self.value = value

    @abstractmethod
    def op(self):
        raise NotImplementedError("Subclasses must implement the op method")

    def __iter__(self):
        yield 'column', self.column
        yield 'op', self.op
        yield 'value', self.value


class Eq(Operators):
    @property
    def op(self):
        return "="


class NotEq(Operators):
    @property
    def op(self):
        return "!="


class Gt(Operators):
    @property
    def op(self):
        return ">"


class Sub(Operators):
    @property
    def op(self):
        return "-"


class Add(Operators):
    @property
    def op(self):
        return "+"

class Gte(Operators):
    @property
    def op(self):
        return ">="


class Lt(Operators):
    @property
    def op(self):
        return "<"


class Lte(Operators):
    @property
    def op(self):
        return "<="


class Lte(Operators):
    @property
    def op(self):
        return "<="


class Contains(Operators):
    @property
    def op(self):
        return "in"


class HasKey(Operators):
    @property
    def op(self):
        return "?"


class GetJson(Operators):
    @property
    def op(self):
        return "->"


class GetValue(Operators):
    @property
    def op(self):
        return "->>"

class NewOP(Operators):
    @property
    def op(self):
        return "&&"
