try:
    import neutron.errors as errors
    import neutron.builtin_types as bt
    import neutron.neutron_main
except ModuleNotFoundError:
    import errors as errors
    import builtin_types as bt
    import neutron_main

from os import path
import numpy as np

traceback_log = []

class Process:
    def __init__(self, tree, filename="?", imported=False):
        self.tree = tree
        self.objects = {}
        self.type = "PROGRAM"
        self.imported = imported
        self.file_path = filename
        self.objects["--file--"] = self.file_path
        self.global_items = {
            "OBJECTS": {},
            "PATHS": [path.join(path.abspath(path.dirname(__file__)), "libs")],
            "BREAK": False,
            "RETURN": False,
        }

        # Dictionary for all types of statements
        self.stmt = {
            "FUNCTION_DECLARATION": self.function_declaration,  # Function declarations
            "VARIABLE_ASSIGNMENT": self.assign_variable,  # Variable assignment
            "FUNCTION_CALL": self.object_call,  # Function calls
            "PYTHON_CODE": self.python_code,  # Inline python code
            "CLASS_DECLARATION": self.class_declaration,  # Class declarations
            "CLASS_ATTRIBUTE_ASSIGNMENT": self.attribute_assignment,  # Class attribute assignment
            "CONDITIONAL": self.conditional,  # Conditionals (if, else, else if)
            "WHILE": self.while_loop,  # While loops
            "FOR": self.for_loop,  # For loops
            "BREAK": self.break_statement,  # Break statement
            "DEL": self.delete_statement,  # Delete statement
            "VARIABLE_OPERATION": self.variable_operation,
            "IMPORT": self.import_statement,
            "LIMPORT": self.limport_statement,
            "SANDBOX": self.sandbox_statement,
        }

    def in_program(self) -> bool:
        """Check if in main program."""
        return True if self.type == "PROGRAM" else False

    def run(self, tree=None):
        """Run the code."""
        if tree is None:
            for line in self.tree:
                if not self.global_items["BREAK"] and not self.global_items["RETURN"]:
                    self.stmt[line[0]](line[1:])
                else:
                    break
        elif tree is not None:
            for line in tree:
                if not self.global_items["BREAK"] and not self.global_items["RETURN"]:
                    self.stmt[line[0]](line[1:])
                else:
                    break

    def break_statement(self, tree):
        """Break out of loop."""
        self.global_items["BREAK"] = True

    def sandbox_statement(self, tree):
        neutron_main.main(f"{str(self.file_path)}::sandbox", tree=tree[0]["PROGRAM"])

    def for_loop(self, tree):
        """Execute a for loop."""
        dictionary = tree[0]
        program = dictionary["PROGRAM"]
        iterable = dictionary["ITERABLE"]
        variable_name = dictionary["VARIABLE"][1]["VALUE"]
        print(self.objects)
        for i in self.eval_expression(iterable):
            if self.global_items["BREAK"]:
                self.global_items["BREAK"] = False
                break
            self.objects[variable_name] = i
            self.run(tree=program)

    def delete_statement(self, tree):
        """Execute a delete statement."""
        _id = tree[0]["ID"]
        if _id in self.global_items["OBJECTS"]:
            del self.global_items["OBJECTS"][_id]
        elif _id in self.objects:
            del self.objects[_id]

    def variable_operation(self, tree):
        """Execute a variable operation."""
        dictionary = tree[0]
        value = self.eval_expression(dictionary["EXPRESSION"])
        operation = dictionary["OPERATION"]
        name = dictionary["ID"]
        if isinstance(dictionary["ID"], str):
            if dictionary["ID"] not in self.objects:
                errors.variable_referenced_before_assignment_error().raise_error(
                    f'object "{name}" referenced before assignment',
                    file=self.file_path,
                    ln=tree[1],
                )

            elif operation == "ADD":
                self.objects[name] += value
            elif operation == "SUB":
                self.objects[name] -= value
            elif operation == "MUL":
                self.objects[name] *= value
            elif operation == "DIV":
                self.objects[name] /= value
            elif operation == "MOD":
                self.objects[name] %= value

        elif isinstance(dictionary["ID"], tuple):
            name = name[1]["EXPRESSION"][1]["VALUE"]
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
                if operation == "ADD":
                    self.objects[name][self.eval_expression(name[1]["INDEX"])] += value
                elif operation == "SUB":
                    self.objects[name][self.eval_expression(name[1]["INDEX"])] -= value
                elif operation == "MUL":
                    self.objects[name][self.eval_expression(name[1]["INDEX"])] *= value
                elif operation == "DIV":
                    self.objects[name][self.eval_expression(name[1]["INDEX"])] /= value
                elif operation == "MOD":
                    self.objects[name][self.eval_expression(name[1]["INDEX"])] %= value

    def while_loop(self, tree):
        """Execute a while loop."""
        dictionary = tree[0]
        condition = dictionary["CONDITION"]
        program = dictionary["PROGRAM"]
        while (
            self.eval_expression(condition) == True
            and self.global_items["BREAK"] == False
        ):
            self.run(tree=program)
        self.global_items["BREAK"] = False

    def limport_statement(self, tree):
        self.import_statement(tree, limport=True)

    def import_statement(self, tree, limport=False):
        dictionary = tree[0]
        path_items = self.eval_expression(dictionary["EXPRESSION"]).value.split("::")
        path_search = (
            path.dirname(self.file_path)
            if path.isdir(path.join(path.dirname(self.file_path), path_items[0]))
            or path.isfile(
                path.join(path.dirname(self.file_path), f"{path_items[0]}.ntn")
            )
            else self.global_items["PATHS"][0]
        )

        for i, path_bit in enumerate(path_items):
            if path.isdir(path.join(path_search, path_bit)):
                path_search = path.join(
                    path_search, path.join(path_bit, "--init--.ntn")
                )
            elif path.isfile(path.join(path_search, f"{path_bit}.ntn")):
                path_search = path.join(path_search, f"{path_bit}.ntn")
            del path_items[i]

        objects = neutron_main.get_objects(path_search)

        if len(path_items) == 0:
            namespace_name = path.basename(path.dirname(path_search))
            if not limport:
                self.global_items["OBJECTS"][namespace_name] = NamespaceObject(
                    objects[1], namespace_name, self.global_items
                )
            else:
                self.objects[namespace_name] = NamespaceObject(
                    objects[1], namespace_name, self.global_items
                )
        elif len(path_items) >= 1:
            namespace_name = path.basename(path.dirname(path_search))
            namespace_object = NamespaceObject(
                objects[1], namespace_name, self.global_items
            )
            for object_part_namespaced in path_items:
                namespace_object = namespace_object.items[object_part_namespaced]
            namespace_name = path_items[-1]
            if not limport:
                self.global_items["OBJECTS"][namespace_name] = namespace_object
            else:
                self.objects[namespace_name] = namespace_object

    def class_declaration(self, tree):
        """Declare a class teplate."""
        dictionary = tree[0]
        name = dictionary["ID"]
        program = dictionary["PROGRAM"]
        if self.in_program():
            self.global_items["OBJECTS"][name] = ClassTemplate(
                program, name, self.global_items
            )
        elif not self.in_program():
            self.objects[name] = ClassTemplate(program, name, self.global_items)

    def class_attribute(self, body):
        """Get an attribute of a certian instance of a class."""
        line = body[1]
        body = body[0]
        if self.type == "FUNCTION" and body["CLASS"] == "this":
            if isinstance(self.objects["this"], ClassTemplate):
                value = self.objects["this"].objects[body["ATTRIBUTE"]]
            else:
                try:
                    value = self.objects["this"].objects[body["ATTRIBUTE"]]
                except KeyError:
                    errors.variable_referenced_before_assignment_error().raise_error(
                        f'object "{body["ATTRIBUTE"]}" referenced before assignment',
                        file=self.file_path,
                        ln=line,
                    )

        else:
            try:
                value = self.eval_expression(body["CLASS"]).objects[body["ATTRIBUTE"]]
            except KeyError:
                errors.variable_referenced_before_assignment_error().raise_error(
                    f'object "{body["ATTRIBUTE"]}" referenced before assignment',
                    file=self.file_path,
                    ln=line,
                )

        return value

    ### Don't Mind The Spaghetti Code Subject to Change ###
    def conditional(self, tree):
        """Execute a conditional statement."""
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
                return
            else:
                for stmt in _elsif:
                    if self.eval_expression(stmt[0]["CONDITION"]) == True:
                        self.run(stmt[0]["CODE"])
                        return
            self.run(tree=_else["CODE"])

    def eval_sub(self, tree):
        """Evaluate a subtaction expresison."""
        return bt.IntType(
            self.eval_expression(tree[0]) - self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_add(self, tree):
        """Evaluate a addition expresison."""
        return bt.IntType(
            self.eval_expression(tree[0]) + self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_mul(self, tree):
        """Evaluate a multiplication expresison."""
        return bt.IntType(
            self.eval_expression(tree[0]) * self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_div(self, tree):
        """Evaluate a division expresison."""
        return bt.IntType(
            self.eval_expression(tree[0]) / self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_mod(self, tree):
        """Evaluate a modulo expresison."""
        return bt.IntType(
            self.eval_expression(tree[0]) % self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_neg(self, tree):
        """Evaluate a negative sign."""
        return -self.eval_expression(tree)

    def eval_pos(self, tree):
        """Evaluate a positive sign."""
        return +self.eval_expression(tree)

    def eval_eqeq(self, tree):
        """Evaluate a logical equals sign."""
        return bt.BoolType(
            self.eval_expression(tree[0]) == self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_not_eqeq(self, tree):
        """Evaluate a logical not equals sign."""
        return bt.BoolType(
            self.eval_expression(tree[0]) != self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_eq_greater(self, tree):
        """Evaluate a logical greater than or equal to sign."""
        return bt.BoolType(
            self.eval_expression(tree[0]) >= self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_eq_less(self, tree):
        """Evaluate a logical less than or equal to sign."""
        return bt.BoolType(
            self.eval_expression(tree[0]) <= self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_less(self, tree):
        """Evaluate a logical less than sign."""
        return bt.BoolType(
            self.eval_expression(tree[0]) < self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_greater(self, tree):
        """Evaluate a logical greater than sign."""
        return bt.BoolType(
            self.eval_expression(tree[0]) > self.eval_expression(tree[1]),
            enter_value=True,
        )

    def eval_and(self, tree):
        """Evaluate a logical AND operator."""
        if self.eval_expression(tree[0]).value == True:
            if self.eval_expression(tree[1]).value == True:
                return bt.BoolType(True, enter_value=True)
            else:
                return bt.BoolType(False, enter_value=True)
        else:
            return bt.BoolType(False, enter_value=True)

    def eval_or(self, tree):
        """Evaluate a logical OR operator."""
        if self.eval_expression(tree[0]).value == True:
            return bt.BoolType(True, enter_value=True)
        elif self.eval_expression(tree[1]).value == True:
            return bt.BoolType(True, enter_value=True)
        else:
            return bt.BoolType(False, enter_value=True)

    def eval_not(self, tree):
        """Evaluate a logical NOT operator."""
        return (
            bt.BoolType(False, enter_value=True)
            if self.eval_expression(tree[0]).value == True
            else bt.BoolType(True, enter_value=True)
        )

    # Defult Types
    @staticmethod
    def eval_int(tree):
        """Evaluate an integer type."""
        value = bt.IntType(tree)
        return value

    @staticmethod
    def eval_float(tree):
        """Evaluate a float type."""
        value = bt.FloatType(tree)
        return value

    @staticmethod
    def eval_string(tree):
        """Evaluate a string type."""
        value = bt.StringType(tree)
        return value

    @staticmethod
    def eval_bool(tree):
        """Evaluate a bool type."""
        value = bt.BoolType(tree)
        return value

    def eval_numpy(self, tree):
        """Evaluate a numpy array type."""
        return bt.NumpyArray(tree, scope=self)

    def eval_list(self, tree):
        """Evaluate a list type."""
        return bt.ListType(tree, scope=self)

    def eval_tuple(self, tree):
        """Evaluate a tuple type."""
        return bt.TupleType(tree, scope=self)

    def get_index(self, tree):
        """Evaluate a get index of collectables statement."""
        tree = tree[0]
        _object = self.eval_expression(tree["EXPRESSION"])
        _index = self.eval_expression(tree["INDEX"])
        return _object[_index]

    @staticmethod
    def eval_null(tree):
        return bt.NullType()

    def eval_assoc_array(self, tree):
        """Evaluate a tuple type."""
        return bt.AssocArray(tree, scope=self)

    def eval_id(self, tree):
        """Evaluate a variable name."""
        name = tree[0]["VALUE"]
        if name in self.global_items["OBJECTS"]:
            value = self.global_items["OBJECTS"][name]
        elif name in self.objects:
            value = self.objects[name]
        else:
            errors.variable_referenced_before_assignment_error().raise_error(
                f'object "{name}" referenced before assignment',
                file=self.file_path,
                ln=tree[1],
            )

        return value

    def eval_expression(self, tree):
        """Return evaluated object that can be used."""
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
            "NULL": self.eval_null,
            "ASSOC_ARRAY": self.eval_assoc_array,
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
        """Return output from inline python code, or run it."""
        code = tree[0]["CODE"]
        var = bt.Namespace(self.objects)
        gvar = bt.Namespace(self.global_items["OBJECTS"])
        if eval_or_not:
            val = eval(code)
            type_val = type(val)
            dictionary = {
                int: bt.IntType,
                float: bt.FloatType,
                bool: bt.BoolType,
                str: bt.StringType,
                np.ndarray: bt.NumpyArray,
                list: bt.ListType,
                tuple: bt.TupleType,
            }
            if type_val in dictionary:
                return dictionary[type_val](val, enter_value=True)
        elif not eval_or_not:
            exec(code)

    def assign_variable(self, tree):
        """Execute an assign variable statement."""
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
                    bt.AssocArray,
                ),
            ):
                self.objects[name][
                    self.eval_expression(dictionary["ID"][1]["INDEX"])
                ] = self.eval_expression(dictionary["EXPRESSION"])

    def object_call(self, tree):
        """Execute a function call."""
        global traceback_log
        dictionary_func = tree[0]
        dictionary = dictionary_func["FUNCTION_ARGUMENTS"]
        new_pos_arguments = []

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
            function_obj = self.eval_expression(dictionary_func["ID"])
            traceback_log.append({"FILE": self.file_path, "LINE": tree[1], "SCOPE": f'{name}'})
            if isinstance(function_obj, ClassTemplate):
                return_value = ClassInstance(
                    function_obj,
                    None,
                    new_pos_arguments,
                    dictionary["KWARGS"],
                    self.global_items,
                )
            elif isinstance(function_obj, Function):
                return_value = function_obj.run_function(
                    new_pos_arguments, dictionary["KWARGS"]
                )
            else:
                try:
                    return_value = function_obj.run_function(
                        new_pos_arguments, dictionary["KWARGS"]
                    )
                except AttributeError:
                    errors.id_not_callable().raise_error(
                        f'object "{name}" not callable', file=self.file_path, ln=tree[1]
                    )

        elif dictionary_func["ID"][0] == "CLASS_ATTRIBUTE":
            attribute = dictionary_func["ID"][1]["ATTRIBUTE"]
            class_obj = self.eval_expression(dictionary_func["ID"][1]["CLASS"])
            traceback_log.append({"FILE": self.file_path, "LINE": tree[1], "SCOPE": f'{dictionary_func["ID"][1]["CLASS"]}::{dictionary_func["ID"][1]["ATTRIBUTE"]}'})
            return_value = class_obj.run_method(
                attribute,
                new_pos_arguments,
                dictionary_func["FUNCTION_ARGUMENTS"]["KWARGS"],
            )

        elif dictionary_func["ID"][0] != "ID":
            object_not_callable = errors.ErrorClass(
                f"{dictionary_func['ID'][0].lower()}_not_callable_error", ln=tree[1]
            )
            object_not_callable.raise_error(
                f"{dictionary_func['ID'][0].lower()} type is not callable",
                file=self.file_path,
                ln=tree[1],
            )

        return return_value

    def function_declaration(self, tree):
        """Declare a function."""
        dictionary = tree[0]
        name = dictionary["ID"]
        arguments = dictionary["FUNCTION_ARGUMENTS"]
        program = dictionary["PROGRAM"]
        if self.in_program():
            self.global_items["OBJECTS"][name] = Function(
                program, name, arguments, self.global_items, filename=self.file_path
            )
        elif not self.in_program():
            self.objects[name] = Function(
                program, name, arguments, self.global_items, filename=self.file_path
            )

    def attribute_assignment(self, tree):
        """Assign an attribute to an instance of a class."""
        tree = tree[0] if isinstance(tree, tuple) else tree
        self.objects[tree["CLASS_ATTRIBUTE"][1]["CLASS"][1]["VALUE"]].objects[
            tree["CLASS_ATTRIBUTE"][1]["ATTRIBUTE"]
        ] = self.eval_expression(tree["EXPRESSION"])


class Function(Process):
    def __init__(self, tree, name, arguments, global_items, filename="?"):
        Process.__init__(self, tree, filename=filename)
        self.name = name
        self.type = "FUNCTION"
        self.arguments = arguments
        self.tree = tree
        self.global_items = global_items
        self.stmt = {
            **self.stmt,
            "CLASS_ATTRIBUTE_ASSIGNMENT": self.attribute_assignment,
            "RETURN": self.return_statement,  # Return statement
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
                    if not isinstance(item["ID"], tuple):
                        self.kw_arguments[item["ID"]] = self.eval_expression(
                            item["EXPRESSION"]
                        )
                    else:
                        self.kw_arguments[
                            item["ID"][1]["VALUE"]
                        ] = self.eval_expression(item["EXPRESSION"])

    def run_function(self, pos_arguments, kw_args):
        kw_arguments = {}

        pos_arguments = [x for x in pos_arguments if x is not None]

        if len(pos_arguments) != len(self.positional_arguments):
            error = errors.positional_argument_error()
            error.raise_error(
                f"{len(self.positional_arguments)} arguments expected {len(pos_arguments)} were found",
                file=self.file_path,
            )

        for i, name in enumerate(self.positional_arguments):
            single_argument = pos_arguments[i]
            self.objects[name] = (
                self.eval_expression(single_argument)
                if isinstance(single_argument, tuple)
                else single_argument
            )

        for item in kw_args:
            if item is None:
                continue
            if not isinstance(item["ID"], tuple):
                kw_arguments[item["ID"]] = self.eval_expression(item["EXPRESSION"])
            else:
                kw_arguments[item["ID"][1]["VALUE"]] = self.eval_expression(
                    item["EXPRESSION"]
                )

        for variable in self.kw_arguments:
            if variable not in kw_arguments:
                self.objects[variable] = self.kw_arguments[variable]
            elif variable in kw_arguments:
                self.objects[variable] = kw_arguments[variable]

        self.run()
        self.global_items["RETURN"] = False
        if "--return--" in self.objects:
            return self.objects["--return--"]
        elif "--return--" not in self.objects:
            return bt.NullType()

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
                    file=self.file_path,
                    ln=tree[1],
                )

    def return_statement(self, tree):
        dictionary = tree[0]
        value = self.eval_expression(dictionary["EXPRESSION"])
        self.global_items["RETURN"] = True
        self.objects["--return--"] = value


class ClassTemplate(Function, Process):
    def __init__(self, tree, name, global_items, filename="?"):
        Process.__init__(self, tree, filename=filename)
        self.stmt = {
            "FUNCTION_DECLARATION": self.function_declaration,
            "CLASS_DECLARATION": self.class_declaration,
            "PYTHON_CODE": self.python_code,
        }
        self.name = name
        self.type = "CLASS_TEMPLATE"
        self.global_items = global_items
        self.run()

        if "--init--" in self.objects:
            self.positional_arguments = self.objects["--init--"].positional_arguments
            self.kw_arguments = self.objects["--init--"].kw_arguments
        else:
            self.positional_arguments, self.kw_arguments = None, None

    def run_method(self, name_func, pos_arguments, kw_arguments):
        objects = {**self.objects, **self.global_items["OBJECTS"]}
        positional_arguments = list((self,) + tuple(pos_arguments))
        return objects[name_func].run_function(positional_arguments, kw_arguments)


class ClassInstance(ClassTemplate):
    def __init__(self, instance, name, pos_arguments, kw_arguments, global_items):
        ClassTemplate.__init__(self, instance.tree, instance.name, global_items)
        self.name = name
        self.type = "CLASS_INSTANCE"
        self.global_items = global_items
        self.run_method("--init--", pos_arguments, kw_arguments)


class NamespaceObject(Process):
    def __init__(self, items, name, global_items):
        self.items = items
        self.name = name
        self.objects = self.items
        self.global_items = global_items

    def run_method(self, name_func, pos_arguments, kw_arguments):
        objects = {**self.items}
        positional_arguments = list((self,) + tuple(pos_arguments))
        if isinstance(objects[name_func], ClassTemplate):
            return ClassInstance(
                objects[name_func],
                name_func,
                pos_arguments,
                kw_arguments,
                self.global_items,
            )
        elif isinstance(objects[name_func], Function):
            return objects[name_func].run_function(
                positional_arguments[1:], kw_arguments
            )
        else:
            print("oh noes something went wrong")
