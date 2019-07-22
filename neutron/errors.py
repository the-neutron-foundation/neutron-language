import platform
import os
import linecache
from neutron_interpreter import traceback_log


class ErrorClass:
    def __init__(self, type):
        self.type = type

    def raise_error(self, msg, ln="?", file="?"):
        if platform.system() == "Windows":
            os.system("color")
        for traceback in traceback_log:
            print(
                f' \033[91mIn file "{traceback["FILE"]}" line {traceback["LINE"]} in {traceback["SCOPE"]};\033[0m'
            )
            print(f'   {linecache.getline(traceback["FILE"], traceback["LINE"]).lstrip()}', end="")
        print(f' \033[91mIn file "{file}" line {ln};\033[0m\n', end="")
        print(f'   {linecache.getline(file, ln).lstrip()}', end="")
        print(f'\033[1m\033[91m{self.type}\033[0m: \033[93m{msg}\033[0m')
        quit()


class syntax_error(ErrorClass):
    def __init__(self):
        self.type = "syntax_error"


class positional_argument_error(ErrorClass):
    def __init__(self):
        self.type = "positional_argument_error"


class id_not_callable(ErrorClass):
    def __init__(self):
        self.type = "id_not_callable"


class variable_referenced_before_assignment_error(ErrorClass):
    def __init__(self):
        self.type = "object_referenced_before_assignment_error"


class type_error(ErrorClass):
    def __init__(self,):
        self.type = "type_error"


class get_error(ErrorClass):
    def __init__(self):
        self.type = "get_error"


class statement_not_expected_error(ErrorClass):
    def __init__(self):
        self.type = "statement_not_expected_error"


class arithmetic_error(ErrorClass):
    def __init__(self):
        self.type = "arithmetic_error"


class logic_operand_error(ErrorClass):
    def __init__(self):
        self.type = "logic_operand_error"


class miscellaneous_error(ErrorClass):
    def __init__(self):
        self.type = "miscellaneous_error"
