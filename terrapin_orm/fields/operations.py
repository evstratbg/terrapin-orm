from abc import abstractmethod
from typing import Any


class Operator:
    def __init__(self, column: str, value: Any):
        self.column = column
        self.value = value

    @abstractmethod
    def op(self):
        raise NotImplementedError("Subclasses must implement the op method")

    def __iter__(self):
        yield "column", self.column
        yield "op", self.op
        yield "value", self.value


class Eq(Operator):
    @property
    def op(self):
        return "="


class NotEq(Operator):
    @property
    def op(self):
        return "!="


class Gt(Operator):
    @property
    def op(self):
        return ">"


class Sub(Operator):
    @property
    def op(self):
        return "-"


class ISub(Sub):
    pass


class Mul(Operator):
    @property
    def op(self):
        return "*"


class IMul(Mul):
    pass


class Div(Operator):
    @property
    def op(self):
        return "/"


class IDiv(Div):
    pass


class Add(Operator):
    @property
    def op(self):
        return "+"


class IAdd(Add):
    pass


class Gte(Operator):
    @property
    def op(self):
        return ">="


class Lt(Operator):
    @property
    def op(self):
        return "<"


class Lte(Operator):
    @property
    def op(self):
        return "<="


class Lte(Operator):
    @property
    def op(self):
        return "<="


class Contains(Operator):
    @property
    def op(self):
        return "in"


class HasKey(Operator):
    @property
    def op(self):
        return "?"


class GetJson(Operator):
    @property
    def op(self):
        return "->"


class GetValue(Operator):
    @property
    def op(self):
        return "->>"
