from numpy import array

try:
    import neutron.errors as errors
except ModuleNotFoundError:
    import errors as errors


def add(item1, item2):
    return item1 + item2


def sub(item1, item2):
    return item1 - item2


def mul(item1, item2):
    return item1 * item2


def div(item1, item2):
    return item1 / item2


def mod(item1, item2):
    return item1 % item2


class DataType:
    def __init__(self, tree, scope=None, enter_value=False):
        self.tree = tree
        self.scope = scope
        self.value = self.eval_tree() if not enter_value else tree
        self.type = int

    def eval_tree(self):
        return None

    def __repr__(self):
        return f"{self.value}"

    def __add__(self, other):
        return (
            add(self.value, other)
            if isinstance(other, self.type)
            else add(self, other.value)
        )

    def __mul__(self, other):
        return (
            mul(self.value, other)
            if isinstance(other, self.type)
            else mul(self, other.value)
        )

    def __sub__(self, other):
        return (
            sub(self.value, other)
            if isinstance(other, self.type)
            else sub(self, other.value)
        )

    def __truediv__(self, other):
        return self.type(
            div(self.value, other)
            if isinstance(other, self.type)
            else div(self, other.value)
        )

    def __mod__(self, other):
        return (
            mod(self.value, other)
            if isinstance(other, self.type)
            else mod(self, other.value)
        )

    def __radd__(self, other):
        return self.__add__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rsub__(self, other):
        return (
            sub(other, self.value)
            if isinstance(other, self.type)
            else sub(other.value, self.value)
        )

    def __rtruediv__(self, other):
        return self.type(
            div(other / self.value)
            if isinstance(other, self.type)
            else div(other.value, self.value)
        )

    def __rmod__(self, other):
        return (
            mod(other, self.value)
            if isinstance(other, self.type)
            else mod(other.value, self.value)
        )

    def __ne__(self, other):
        return (
            other != self.value
            if isinstance(other, self.type)
            else other.value != self.value
        )

    def __lt__(self, other):
        return (
            other > self.value
            if isinstance(other, self.type)
            else other.value > self.value
        )

    def __gt__(self, other):
        return (
            other < self.value
            if isinstance(other, self.type)
            else other.value < self.value
        )

    def __eq__(self, other):
        return (
            self.value == other
            if isinstance(other, self.type)
            else self.value == other.value
        )

    def __le__(self, other):
        return (
            self.value <= other
            if isinstance(other, self.type)
            else self.value <= other.value
        )

    def __ge__(self, other):
        return (
            self.value >= other
            if isinstance(other, self.type)
            else self.value >= other.value
        )

    def __int__(self):
        return int(self.value)

    def __long__(self):
        return long(self.value)

    def __float__(self):
        return float(self.value)

    def __complex__(self):
        return complex(self.value)

    def __oct__(self):
        return oct(self.value)

    def __hex__(self):
        return hex(self.value)

    def __getitem__(self, index):
        return self.value[index.value]

    def __setitem__(self, key, value):
        self.value[key.value] = value

    def __iter__(self):
        return iter(self.value)

    def __len__(self):
        return len(self.value)


class IntType(DataType):
    def eval_tree(self):
        return int(self.tree[0]["VALUE"])


class FloatType(DataType):
    def __init__(self, tree, scope=None, enter_value=False):
        DataType.__init__(self, tree, scope=scope, enter_value=enter_value)
        self.type = float

    def eval_tree(self):
        return float(self.tree[0]["VALUE"])


class StringType(DataType):
    def __init__(self, tree, scope=None, enter_value=False):
        DataType.__init__(self, tree, scope=scope, enter_value=enter_value)
        self.type = str

    def eval_tree(self):
        return str(self.tree[0]["VALUE"])


class BoolType(DataType):
    def __init__(self, tree, scope=None, enter_value=False):
        DataType.__init__(self, tree, scope=scope, enter_value=enter_value)
        self.type = bool

    def eval_tree(self):
        value = self.tree[0]["VALUE"]
        return True if value == "true" else False

    def __str__(self):
        return "true" if self.value else "false"


class NumpyArray(DataType):
    def __init__(self, tree, scope=None, enter_value=False):
        DataType.__init__(self, tree, scope=scope, enter_value=enter_value)
        self.type = array

    def eval_tree(self):
        tree = self.tree[0]["ITEMS"]
        value = []
        for item in tree:
            value.append(self.scope.eval_expression(item))
        return array(value)

    def __str__(self):
        return f"({self.value.__str__()[1:-1]})"


class ListType(DataType):
    def __init__(self, tree, scope=None, enter_value=False):
        DataType.__init__(self, tree, scope=scope, enter_value=enter_value)
        self.type = list

    def eval_tree(self):
        tree = self.tree[0]["ITEMS"]
        value = []
        for item in tree:
            value.append(self.scope.eval_expression(item))
        return list(value)

    def __str__(self):
        return self.value.__str__()


class TupleType(DataType):
    def __init__(self, tree, scope=None, enter_value=False):
        DataType.__init__(self, tree, scope=scope, enter_value=enter_value)
        self.type = tuple

    def eval_tree(self):
        tree = self.tree[0]["ITEMS"]
        value = ()
        for item in tree:
            value = value + (self.scope.eval_expression(item),)
        return value

    def __str__(self):
        return f"{{{self.value.__str__()[1:-1]}}}"


class NullType:
    def __init__(self, scope=None, enter_value=False):
        self.type = "null"
        self.value = self.type

    @staticmethod
    def arithmetic_magic_method(other):
        arithmetic = errors.arithmetic_error()
        arithmetic.raise_error("Arithmetic not supported with the NullType type")

    @staticmethod
    def logic_magic_method(other):
        arithmetic = errors.logic_operand_error()
        arithmetic.raise_error(
            "Logical operations not supported with the NullType type"
        )

    @staticmethod
    def conversion_magic_method(other):
        arithmetic = errors.type_error()
        arithmetic.raise_error(
            "Conversion of types not supported with the NullType type"
        )

    @staticmethod
    def miscellaneous_magic_method(other):
        arithmetic = errors.miscellaneous_error()
        arithmetic.raise_error("Operation not supported with the NullType type")

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        return True if isinstance(other, NullType) else False

    __add__ = arithmetic_magic_method
    __sub__ = arithmetic_magic_method
    __truediv__ = arithmetic_magic_method
    __mod__ = arithmetic_magic_method
    __mul__ = arithmetic_magic_method

    __ne__ = logic_magic_method
    __gt__ = logic_magic_method
    __lt__ = logic_magic_method
    __ge__ = logic_magic_method
    __le__ = logic_magic_method

    __int__ = conversion_magic_method
    __long__ = conversion_magic_method
    __float__ = conversion_magic_method
    __oct__ = conversion_magic_method
    __complex__ = conversion_magic_method
    __hex__ = conversion_magic_method

    __len__ = miscellaneous_magic_method
    __iter__ = miscellaneous_magic_method
    __setitem__ = miscellaneous_magic_method
    __getitem__ = miscellaneous_magic_method


class Namespace:
    def __init__(self, adict):
        self.variables = adict
        self.__dict__.update(adict)

    def __setattr__(self, name, value):
        self.__dict__.update({name: value})
        self.variables.update({name: value})
