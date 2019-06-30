try:
    import neutron.errors as errors
    import neutron.builtin_types as bt
except ModuleNotFoundError:
    import errors as errors
    import builtin_types as bt

from os import path
import numpy as np

global global_objects, paths_to_look_in, global_break
global_break = False
global_objects = {}
paths_to_look_in = [path.abspath(__file__)]


class Process:
    def __init__(self, tree, filename="?"):
        self.tree = tree
        self.objects = {}
        self.type = "PROGRAM"
        self.file_path = filename
        self.stmt = {
            "FUNCTION_DECLARATION": self.function_declaration,
            "VARIABLE_ASSIGNMENT": self.assign_variable,
            "FUNCTION_CALL": self.object_call,
            "PYTHON_CODE": self.python_code,
            "CLASS_DECLARATION": self.class_declaration,
            "CLASS_ATTRIBUTE_ASSIGNMENT": self.attribute_assignment,
            "CONDITIONAL": self.conditional,
            "WHILE": self.while_loop,
            "FOR": self.for_loop,
            "BREAK": self.break_statement,
            "DEL": self.delete_statement,
        }

    def in_program(self):
        return True if self.type == "PROGRAM" else False

    def run(self, tree=None):
        if tree is None:
            for line in self.tree:
                if not global_break:
                    self.stmt[line[0]](line[1:])
                else:
                    break
        elif tree is not None:
            for line in tree:
                if not global_break:
                    self.stmt[line[0]](line[1:])
                else:
                    break

    def break_statement(self, tree):
        global global_break
        global_break = True

    def for_loop(self, tree):
        global global_break
        dictionary = tree[0]
        program = dictionary["PROGRAM"]
        iterable = dictionary["ITERABLE"]
        variable_name = dictionary["VARIABLE"][1]["VALUE"]
        for i in self.eval_expression(iterable):
            if global_break:
                global_break = False
                break
            self.objects[variable_name] = i
            self.run(tree=program)

    def delete_statement(self, tree):
        id = tree[0]["ID"]
        if id in global_objects:
            del global_objects[id]
        elif id in self.objects:
            del self.objects[id]

    def while_loop(self, tree):
        global global_break
        dictionary = tree[0]
        condition = dictionary["CONDITION"]
        program = dictionary["PROGRAM"]
        while self.eval_expression(condition) == True and global_break == False:
            self.run(tree=program)
        global_break = False

    def eval_id(self, tree):
        name = tree[0]["VALUE"]
        if name in global_objects:
            value = global_objects[name]
        elif name in self.objects:
            value = self.objects[name]
        else:
            errors.variable_referenced_before_assignment_error().raise_error(
                f'variable "{name}" referenced before assignment',
                file=global_objects["--file--"],
            )

        return value

    def class_declaration(self, tree):
        dictionary = tree[0]
        name = dictionary["ID"]
        program = dictionary["PROGRAM"]
        if self.in_program():
            global_objects[name] = ClassTemplate(program, name)
        elif not self.in_program():
            self.objects[name] = ClassTemplate(program, name)

    def class_attribute(self, body):
        body = body[0]
        if self.type == "FUNCTION" and body["CLASS"] == "this":
            if isinstance(self.objects["this"], ClassTemplate):
                value = self.objects["this"].objects[body["ATTRIBUTE"]]
            else:
                try:
                    value = self.objects["this"].objects[body["ATTRIBUTE"]]
                except KeyError:
                    errors.variable_referenced_before_assignment_error().raise_error(
                        f'variable "{name}" referenced before assignment',
                        file=global_objects["--file--"],
                    )

        else:
            classes = {**self.objects, **global_objects}
            value = classes[body["CLASS"][1]["VALUE"]].objects[body["ATTRIBUTE"]]

        return value

    ### Don't Mind The Spaghetti Code Subject to Change ###
    def conditional(self, tree):
        dictionary = tree[0]
        _if = dictionary["IF"][1]
        _elsif = dictionary["ELSE_IF"][1:]
        _else = dictionary["ELSE"][1]
        if _if != None and _elsif[0] == None and _else == None:
            if self.eval_expression(_if["CONDITION"]) == True:
                self.run(tree=_if["CODE"])
        elif _if != None and _elsif[0] == None and _else != None:
            if self.eval_expression(_if["CONDITION"]) == True:
                self.run(tree=_if["CODE"])
            else:
                self.run(tree=_else["CODE"])
        elif _if != None and _elsif[0] != None and _else == None:
            if self.eval_expression(_if["CONDITION"]) == True:
                self.run(tree=_if["CODE"])
            else:
                is_true = False
                for stmt in _elsif:
                    if (
                        self.eval_expression(stmt[0]["CONDITION"]) == True
                        and not is_true
                    ):
                        is_true = True
                        self.run(stmt[0]["CODE"])
        elif _if != None and _elsif[0] != None and _else != None:
            if self.eval_expression(_if["CONDITION"]) == True:
                self.run(tree=_if["CODE"])
            else:
                for stmt in _elsif:
                    if self.eval_expression(stmt[0]["CONDITION"]) == True:
                        self.run(stmt[0]["CODE"])
                        return
            self.run(tree=_else["CODE"])

    def eval_sub(self, tree):
        return bt.IntType(
            self.eval_expression(tree[0]) - self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_add(self, tree):
        return bt.IntType(
            self.eval_expression(tree[0]) + self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_mul(self, tree):
        return bt.IntType(
            self.eval_expression(tree[0]) * self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_div(self, tree):
        return bt.IntType(
            self.eval_expression(tree[0]) / self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_mod(self, tree):
        return bt.IntType(
            self.eval_expression(tree[0]) % self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_neg(self, tree):
        return -self.eval_expression(tree)

    def eval_pos(self, tree):
        return +self.eval_expression(tree)

    def eval_eqeq(self, tree):
        return bt.BoolType(
            self.eval_expression(tree[0]) == self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_not_eqeq(self, tree):
        return bt.BoolType(
            self.eval_expression(tree[0]) != self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_eq_greater(self, tree):
        return bt.BoolType(
            self.eval_expression(tree[0]) >= self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_eq_less(self, tree):
        return bt.BoolType(
            self.eval_expression(tree[0]) <= self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_less(self, tree):
        return bt.BoolType(
            self.eval_expression(tree[0]) < self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_greater(self, tree):
        return bt.BoolType(
            self.eval_expression(tree[0]) > self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_and(self, tree):
        if self.eval_expression(tree[0]).value == True:
            if self.eval_expression(tree[1]).value == True:
                return bt.BoolType(True, enter_value=True)
            else:
                return bt.BoolType(False, enter_value=True)
        else:
            return bt.BoolType(False, enter_value=True)

    def eval_or(self, tree):
        if self.eval_expression(tree[0]).value == True:
            return bt.BoolType(True, enter_value=True)
        elif self.eval_expression(tree[1]).value == True:
            return bt.BoolType(True, enter_value=True)
        else:
            return bt.BoolType(False, enter_value=True)

    def eval_not(self, tree):
        return (
            bt.BoolType(False, enter_value=True)
            if self.eval_expression(tree[0]).value == True
            else bt.BoolType(True, enter_value=True)
        )

    # Defult Types
    @staticmethod
    def eval_int(tree):
        value = bt.IntType(tree)
        return value

    @staticmethod
    def eval_float(tree):
        value = bt.FloatType(tree)
        return value

    @staticmethod
    def eval_string(tree):
        value = bt.StringType(tree)
        return value

    @staticmethod
    def eval_bool(tree):
        value = bt.BoolType(tree)
        return value

    def eval_numpy(self, tree):
        return bt.NumpyArray(tree, scope=self)

    def eval_list(self, tree):
        return bt.ListType(tree, scope=self)

    def eval_tuple(self, tree):
        return bt.TupleType(tree, scope=self)

    def get_index(self, tree):
        tree = tree[0]
        _object = self.eval_expression(tree["EXPRESSION"])
        _index = self.eval_expression(tree["INDEX"])
        return _object[_index]

    def eval_expression(self, tree):
        _type = tree[0]
        body = tree[1:]
        value = "something went wrong tell developers"
        type_to_function = {
            # Data Types
            "INT": self.eval_int,
            "FLOAT": self.eval_float,
            "BOOL": self.eval_bool,
            "STRING": self.eval_string,
            "ID": self.eval_id,
            "NUMPY": self.eval_numpy,
            "LIST": self.eval_list,
            "TUPLE": self.eval_tuple,
            # Bin Ops
            "SUB": self.eval_sub,
            "ADD": self.eval_add,
            "MUL": self.eval_mul,
            "DIV": self.eval_div,
            "MOD": self.eval_mod,
            "NEG": self.eval_neg,
            "POS": self.eval_pos,
            # Bool Ops
            "EQEQ": self.eval_eqeq,
            "NOT_EQEQ": self.eval_not_eqeq,
            "EQ_LESS": self.eval_eq_less,
            "EQ_GREATER": self.eval_eq_greater,
            "OR": self.eval_or,
            "NOT": self.eval_not,
            "AND": self.eval_and,
            "GREATER": self.eval_greater,
            "LESS": self.eval_less,
            # Functionality
            "FUNCTION_CALL": self.object_call,
            "CLASS_ATTRIBUTE": self.class_attribute,
            "GET_INDEX": self.get_index,
        }
        if _type in type_to_function:
            value = type_to_function[_type](body)
        elif _type == "PYTHON_CODE":
            value = self.python_code(body, eval_or_not=True)
        return value

    ### End of Spaghetti Code *relief* ###

    def python_code(self, tree, eval_or_not=False):
        code = tree[0]["CODE"]
        var = bt.Namespace(self.objects)
        gvar = bt.Namespace(global_objects)
        if eval_or_not:
            return eval(code)
        elif not eval_or_not:
            exec(code)

    def assign_variable(self, tree):
        dictionary = tree[0]
        value = self.eval_expression(dictionary["EXPRESSION"])
        if isinstance(dictionary["ID"], str):
            self.objects[dictionary["ID"]] = value
        elif isinstance(dictionary["ID"], tuple):
            name = dictionary["ID"][1]["EXPRESSION"][1]["VALUE"]
            variable = self.objects[name]
            if isinstance(
                variable,
                (
                    bt.ListType,
                    ClassInstance,
                    bt.StringType,
                    bt.NumpyArray,
                    bt.TupleType,
                ),
            ):
                self.objects[name][
                    self.eval_expression(dictionary["ID"][1]["INDEX"])
                ] = self.eval_expression(dictionary["EXPRESSION"])

    def get_variable(self, name):
        if name in global_objects:
            return global_objects[name]
        elif name in self.objects:
            return self.objects[name]
        else:
            errors.variable_referenced_before_assignment_error().raise_error(
                f'variable "{name}" referenced before assignment',
                file=global_objects["--file--"],
            )

    def object_call(self, tree):
        dictionary_func = tree[0]
        dictionary = dictionary_func["FUNCTION_ARGUMENTS"]
        new_pos_arguments = []
        objects = {**self.objects, **global_objects}

        if "POSITIONAL_ARGS" in dictionary:
            if None not in dictionary["POSITIONAL_ARGS"]:
                for expr in dictionary["POSITIONAL_ARGS"]:
                    new_pos_arguments.append(self.eval_expression(expr))

        elif "POSITIONAL_ARGS" not in dictionary:
            dictionary["POSITIONAL_ARGS"] = (None,)
        if "KWARGS" not in dictionary:
            dictionary["KWARGS"] = (None,)

        if dictionary_func["ID"][0] == "ID":
            name = dictionary_func["ID"][1]["VALUE"]
            if name in objects and isinstance(objects[name], ClassTemplate):
                return_value = ClassInstance(
                    objects[name], None, new_pos_arguments, dictionary["KWARGS"]
                )
            elif name not in objects:
                errors.variable_referenced_before_assignment_error().raise_error(
                    f'object "{name}" referenced before assignment',
                    file=global_objects["--file--"],
                )
            elif isinstance(objects[name], Function):
                return_value = objects[name].run_function(
                    new_pos_arguments, dictionary["KWARGS"]
                )
            else:
                try:
                    return_value = objects[name].run_function(
                        new_pos_arguments, dictionary["KWARGS"]
                    )
                except AttributeError:
                    errors.id_not_callable().raise_error(
                        f'object "{name}" not callable',
                        file=global_objects["--file--"],
                    )

        elif dictionary_func["ID"][0] == "CLASS_ATTRIBUTE":
            if self.type == "PROGRAM":
                attribute = dictionary_func["ID"][1]["ATTRIBUTE"]
                class_name = dictionary_func["ID"][1]["CLASS"][1]["VALUE"]
                return_value = objects[class_name].run_method(
                    attribute,
                    dictionary_func["FUNCTION_ARGUMENTS"]["POSITIONAL_ARGS"],
                    dictionary_func["FUNCTION_ARGUMENTS"]["KWARGS"],
                )
            elif self.type == "FUNCTION":
                if isinstance(self.positional_arguments[0], ClassTemplate):
                    attribute = dictionary_func["ID"][1]["ATTRIBUTE"]
                    class_name = dictionary_func["ID"][1]["CLASS"]
                    return_value = objects[class_name].run_method(
                        attribute,
                        dictionary_func["FUNCTION_ARGUMENTS"]["POSITIONAL_ARGS"],
                        dictionary_func["FUNCTION_ARGUMENTS"]["KWARGS"],
                    )

        elif dictionary_func["ID"][0] != "ID":
            object_not_callable = errors.ErrorClass(
                f"{dictionary_func['ID'][0].lower()}_not_callable_error"
            )
            object_not_callable.raise_error(
                f"{dictionary_func['ID'][0].lower()} type is not callable",
                file=global_objects["--file--"],
            )

        return return_value

    def function_declaration(self, tree):
        dictionary = tree[0]
        name = dictionary["ID"]
        arguments = dictionary["FUNCTION_ARGUMENTS"]
        program = dictionary["PROGRAM"]
        if self.in_program():
            global_objects[name] = Function(program, name, arguments)
        elif not self.in_program():
            self.objects[name] = Function(program, name, arguments)

    def attribute_assignment(self, tree):
        tree = tree[0] if isinstance(tree, tuple) else tree
        self.objects[tree["CLASS_ATTRIBUTE"][1]["CLASS"][1]["VALUE"]].objects[
            tree["CLASS_ATTRIBUTE"][1]["ATTRIBUTE"]
        ] = self.eval_expression(tree["EXPRESSION"])


class Function(Process):
    def __init__(self, tree, name, arguments):
        Process.__init__(self, tree)
        self.name = name
        self.type = "FUNCTION"
        self.arguments = arguments
        self.tree = tree
        self.stmt = {
            **self.stmt,
            "CLASS_ATTRIBUTE_ASSIGNMENT": self.attribute_assignment,
        }
        self.positional_arguments = []
        self.kw_arguments = {}
        self.evaluate_arguments()

    def evaluate_arguments(self):
        for key in self.arguments:
            if key == "POSITIONAL_ARGS":
                for item in self.arguments[key]:
                    self.positional_arguments.append(item[1]["VALUE"])
            if key == "KWARGS":
                for item in self.arguments[key]:
                    self.kw_arguments[item["ID"]] = self.eval_expression(
                        item["EXPRESSION"]
                    )

    def run_function(self, pos_arguments, kw_args):
        kw_arguments = {}

        pos_arguments = [x for x in pos_arguments if x is not None]

        if len(pos_arguments) != len(self.positional_arguments):
            error = errors.positional_argument_error()
            error.raise_error(
                f"{len(self.positional_arguments)} arguments expected {len(pos_arguments)} were found",
                file=global_objects["--file--"],
            )

        for i, name in enumerate(self.positional_arguments):
            single_argument = pos_arguments[i]
            self.objects[name] = (
                self.eval_expression(single_argument)
                if isinstance(single_argument, tuple)
                else single_argument
            )

        # try:
        for item in kw_args:
            if item is None:
                continue
            kw_arguments[item["ID"]] = self.eval_expression(item["EXPRESSION"])

        for variable in self.kw_arguments:
            if variable not in kw_arguments:
                self.objects[variable] = self.kw_arguments[variable]
            elif variable in kw_arguments:
                self.objects[variable] = kw_arguments[variable]

        # except TypeError:
        #    pass

        self.run()
        if "--return--" in self.objects:
            return self.objects["--return--"]
        elif "--return--" not in self.objects:
            return None

    def attribute_assignment(self, tree):
        dictionary = tree[0]
        dictionary = dictionary[0] if isinstance(dictionary, tuple) else dictionary
        if "this" in self.objects and isinstance(self.objects["this"], ClassTemplate):
            if dictionary["CLASS_ATTRIBUTE"][1]["CLASS"][1]["VALUE"] == "this":
                attribute = dictionary["CLASS_ATTRIBUTE"][1]["ATTRIBUTE"]
                self.objects["this"].objects[attribute] = self.eval_expression(
                    dictionary["EXPRESSION"]
                )
        else:
            try:
                self.objects[
                    dictionary["CLASS_ATTRIBUTE"][1]["CLASS"][1]["VALUE"]
                ].objects[
                    dictionary["CLASS_ATTRIBUTE"][1]["ATTRIBUTE"]
                ] = self.eval_expression(
                    dictionary["EXPRESSION"]
                )
            except KeyError:
                errors.variable_referenced_before_assignment_error().raise_error(
                    f'object "{dictionary["CLASS_ATTRIBUTE"][1]["ATTRIBUTE"]}" referenced before assignment',
                    file=global_objects["--file--"],
                )


class ClassTemplate(Function):
    def __init__(self, tree, name):
        Process.__init__(self, tree)
        self.stmt = {"FUNCTION_DECLARATION": self.function_declaration}
        self.name = name
        self.type = "CLASS_TEMPLATE"
        self.run()

        if "--init--" in self.objects:
            self.positional_arguments = self.objects["--init--"].positional_arguments
            self.kw_arguments = self.objects["--init--"].kw_arguments
        else:
            self.positional_arguments, self.kw_arguments = None, None

    def run_method(self, name_func, pos_arguments, kw_arguments):
        objects = {**self.objects, **global_objects}
        positional_arguments = list((self,) + tuple(pos_arguments))
        return objects[name_func].run_function(positional_arguments, kw_arguments)


class ClassInstance(ClassTemplate):
    def __init__(self, instance, name, pos_arguments, kw_arguments):
        ClassTemplate.__init__(self, instance.tree, instance.name)
        self.name = name
        self.type = "CLASS_INSTANCE"
        self.run_method("--init--", pos_arguments, kw_arguments)
