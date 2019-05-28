class DataType:
    def __init__(self, tree, scope=None, enter_value=False):
        self.tree = tree
        self.scope = scope
        self.value = self.eval_tree() if not enter_value else tree

    def eval_tree(self):
        return None

    def __repr__(self):
        return f"neutron::{self.__class__.__name__} <value: {self.value}>"
    def __add__(self, other):
        return self.value + other if isinstance(other, int) else self.value + other.value
    def __mul__(self, other):
        return self.value * other if isinstance(other, int) else self.value * other.value
    def __sub__(self, other):
        return self.value - other if isinstance(other, int) else self.value - other.value
    def __truediv__(self, other):
        return self.value / other if isinstance(other, int) else self.value / other.value
    def __mod__(self, other):
        return self.value % other if isinstance(other, int) else self.value % other.value

    def __radd__(self, other): return self.__add__(other)
    def __rmul__(self, other): return self.__mul__(other)
    def __rsub__(self, other):
        return other + self.value if isinstance(other, int) else other.value + self.value
    def __rtruediv__(self, other):
        return other / self.value if isinstance(other, int) else other.value / self.value
    def __rmod__(self, other):
        return other % self.value if isinstance(other, int) else other.value % self.value

    def __req__(self, other):
        return other == self.value if isinstance(other, int) else other.value == self.value
    def __ne__(self, other):
        return other != self.value if isinstance(other, int) else other.value != self.value
    def __lt__(self, other):
        return other < self.value if isinstance(other, int) else other.value < self.value
    def __gt__(self, other):
        return other > self.value if isinstance(other, int) else other.value > self.value
    def __le__(self, other):
        return other <= self.value if isinstance(other, int) else other.value <= self.value
    def __ge__(self, other):
        return other >= self.value if isinstance(other, int) else other.value >= self.value

    def __eq__(self, other):
        return self.value == other if isinstance(other, int) else self.value == other.value
    def __ne__(self, other):
        return self.value != other if isinstance(other, int) else self.value != other.value
    def __lt__(self, other):
        return self.value < other if isinstance(other, int) else self.value < other.value
    def __gt__(self, other):
        return self.value > other if isinstance(other, int) else self.value > other.value
    def __le__(self, other):
        return self.value <= other if isinstance(other, int) else self.value <= other.value
    def __ge__(self, other):
        return self.value >= other if isinstance(other, int) else self.value >= other.value


class IntType(DataType):
    def eval_tree(self):
        return int(self.tree[0]["VALUE"])


class FloatType(DataType):
    def eval_tree(self):
        return float(self.tree[0]["VALUE"])


class StringType(DataType):
    def eval_tree(self):
        return str(self.tree[0]["VALUE"])


class BoolType(DataType):
    def eval_tree(self):
        value = self.tree[0]["VALUE"]
        return True if value == "true" else False
    def __str__(self):
        return self.tree[0]["VALUE"]

class NumpyArray(DataType):
    def eval_tree(self):
        tree = self.tree[0]["ITEMS"]
        value = []
        for item in tree:
            value.append(self.scope.eval_expression(item))
        return array(value)
    def __str__(self):
        return f"({self.value.__str__()[1:-1]})"


class ListType(DataType):
    def eval_tree(self):
        tree = self.tree[0]["ITEMS"]
        value = []
        for item in tree:
            value.append(self.scope.eval_expression(item))
        return list(value)
    def __str__(self):
        return self.value.__str__()


class TupleType(DataType):
    def eval_tree(self):
        tree = self.tree[0]["ITEMS"]
        value = ()
        for item in tree:
            value = value + (self.scope.eval_expression(item), )
        return value
    def __str__(self):
        return self.value.__str__()
