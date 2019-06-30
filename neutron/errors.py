class ErrorClass:
    def __init__(self, type):
        self.type = type

    def raise_error(self, msg, ln="?", col="?", file="?"):
        print(f"in file: {file} line: {ln} column: {col}\nneutron::{self.type}: {msg}.")
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
