class DataType:
    def __init__(self, tree, scope=None):
        self.tree = tree
        self.scope = scope
        self.value = self.eval_tree()

    def eval_tree(self):
        return None

    def __repr__(self):
        return f"neutron::{self.__class__.__name__} <value: {self.value}>"
    def __add__(self, other):
        return self.value + other.value
    def __mul__(self, other):
        return self.value * other.value
    def __sub__(self, other):
        return self.value - other.value
    def __truediv__(self, other):
        return self.value / other.value
    def __mod__(self, other):
        return self.value % other.value
    def __eq__(self, other):
        return self.value == other.value
    def __ne__(self, other):
        return self.value != other.value
    def __lt__(self, other):
        return self.value < other.value
    def __gt__(self, other):
        return self.value > other.value
    def __le__(self, other):
        return self.value <= other.value
    def __ge__(self, other):
        return self.value >= other.value


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
    def __eq__(self, other):
        try:
            return self.value == other.value
        except AttributeError:
            return self.value == other
    def __ne__(self, other):
        try:
            return self.value != other.value
        except AttributeError:
            return self.value != other
    def __lt__(self, other):
        try:
            return self.value < other.value
        except AttributeError:
            return self.value < other
    def __gt__(self, other):
        try:
            return self.value > other.value
        except AttributeError:
            return self.value > other
    def __le__(self, other):
        try:
            return self.value <= other.value
        except AttributeError:
            return self.value <= other
    def __ge__(self, other):
        try:
            return self.value >= other.value
        except AttributeError:
            return self.value >= other

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
