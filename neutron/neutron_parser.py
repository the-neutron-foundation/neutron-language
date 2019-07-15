try:
    from neutron.neutron_lexer import NeutronLexer
    from neutron.errors import syntax_error
except ModuleNotFoundError:
    from neutron_lexer import NeutronLexer
    from errors import syntax_error
from sly import Parser
import pprint
import logging


class NeutronParser(Parser):
    tokens = NeutronLexer.tokens
    debugfile = "parser.out"
    log = logging.getLogger()
    log.setLevel(logging.ERROR)
    syntax_error_obj = syntax_error()

    precedence = (
        ("left", EMPTY),
        ("left", ","),
        ("right", "="),
        ("left", "|"),
        ("left", "&"),
        ("left", EQEQ, NOT_EQEQ),
        ("left", EQ_LESS, EQ_GREATER, "<", ">"),
        ("left", "+", "-"),
        ("left", "*", "/", "%"),
        ("right", UMINUS, UPLUS),
        ("right", "!"),
        ("left", COLON_COLON),
    )

    # Program START
    @_("program statement")
    def program(self, p):
        return p.program + (p.statement,)

    @_("statement")
    def program(self, p):
        return (p.statement,)

    @_("empty")
    def program(self, p):
        return ()

    # Program END
    ###########################################################################
    # Statements START

    @_("function_declaration")
    def statement(self, p):
        return p.function_declaration + ()

    @_("class_declaration")
    def statement(self, p):
        return p.class_declaration

    @_("function_call_statement")
    def statement(self, p):
        return p.function_call_statement

    @_("class_attribute_assignment")
    def statement(self, p):
        return p.class_attribute_assignment

    @_("conditional")
    def statement(self, p):
        return p.conditional

    @_("while_loop")
    def statement(self, p):
        return p.while_loop

    @_("python_code_statement")
    def statement(self, p):
        return p.python_code_statement

    @_("variable_assignment")
    def statement(self, p):
        return p.variable_assignment

    @_("break_statement")
    def statement(self, p):
        return p.break_statement

    @_("for_loop")
    def statement(self, p):
        return p.for_loop

    @_("delete_statement")
    def statement(self, p):
        return p.delete_statement

    @_("return_statement")
    def statement(self, p):
        return p.return_statement

    @_("variable_operation")
    def statement(self, p):
        return p.variable_operation

    @_("import_statement")
    def statement(self, p):
        return p.import_statement

    # Statements END
    ###########################################################################
    # Statment syntax START

    @_("function_call ';'")
    def function_call_statement(self, p):
        return p.function_call

    @_("python_code ';'")
    def python_code_statement(self, p):
        return p.python_code

    @_("BREAK ';'")
    def break_statement(self, p):
        return ("BREAK",)

    @_("RETURN expression ';'")
    def return_statement(self, p):
        return ("RETURN", {"EXPRESSION": p.expression})

    @_("expression '(' function_arguments ')'")
    def function_call(self, p):
        return (
            "FUNCTION_CALL",
            {"FUNCTION_ARGUMENTS": p.function_arguments, "ID": p.expression},
        )

    @_("expression '(' empty ')'")
    def function_call(self, p):
        return ("FUNCTION_CALL", {"FUNCTION_ARGUMENTS": {}, "ID": p.expression})

    @_("FUNC ID '(' function_arguments ')' '{' program '}'")
    def function_declaration(self, p):
        return (
            "FUNCTION_DECLARATION",
            {
                "FUNCTION_ARGUMENTS": p.function_arguments,
                "ID": p.ID,
                "PROGRAM": p.program,
            },
        )

    @_("FUNC ID '(' empty ')' '{' program '}'")
    def function_declaration(self, p):
        return (
            "FUNCTION_DECLARATION",
            {"FUNCTION_ARGUMENTS": {}, "ID": p.ID, "PROGRAM": p.program},
        )

    @_("positional_args")
    def function_arguments(self, p):
        return {"POSITIONAL_ARGS": p.positional_args}

    @_("positional_args ',' kwargs")
    def function_arguments(self, p):
        return {"POSITIONAL_ARGS": p.positional_args, "KWARGS": p.kwargs}

    @_("kwargs")
    def function_arguments(self, p):
        return {"KWARGS": p.kwargs}

    @_("CLASS ID '{' program '}'")
    def class_declaration(self, p):
        return ("CLASS_DECLARATION", {"ID": p.ID, "PROGRAM": p.program})

    @_("FOR expression IN expression '{' program '}'")
    def for_loop(self, p):
        return (
            "FOR",
            {
                "PROGRAM": p.program,
                "VARIABLE": p.expression0,
                "ITERABLE": p.expression1,
            },
        )

    @_("WHILE '(' expression ')' '{' program '}'")
    def while_loop(self, p):
        return ("WHILE", {"PROGRAM": p.program, "CONDITION": p.expression})

    @_("positional_args ',' expression")
    def positional_args(self, p):
        return p.positional_args + (p.expression,)

    @_("expression")
    def positional_args(self, p):
        return (p.expression,)

    @_("kwargs ',' id '=' expression")
    def kwargs(self, p):
        return p.kwargs + ({"ID": p.id, "EXPRESSION": p.expression},)

    @_("ID '=' expression")
    def kwargs(self, p):
        return ({"ID": p.ID, "EXPRESSION": p.expression},)

    @_("ID '=' expression ';'")
    def variable_assignment(self, p):
        return ("VARIABLE_ASSIGNMENT", {"ID": p.ID, "EXPRESSION": p.expression})

    @_("get_index '=' expression ';'")
    def variable_assignment(self, p):
        return ("VARIABLE_ASSIGNMENT", {"ID": p.get_index, "EXPRESSION": p.expression})

    @_("ID EQ_ADD expression ';'")
    def variable_operation(self, p):
        return (
            "VARIABLE_OPERATION",
            {"ID": p.ID, "EXPRESSION": p.expression, "OPERATION": "ADD"},
        )

    @_("get_index EQ_ADD expression ';'")
    def variable_operation(self, p):
        return (
            "VARIABLE_OPERATION",
            {"ID": p.get_index, "EXPRESSION": p.expression, "OPERATION": "ADD"},
        )

    @_("ID EQ_SUB expression ';'")
    def variable_operation(self, p):
        return (
            "VARIABLE_OPERATION",
            {"ID": p.ID, "EXPRESSION": p.expression, "OPERATION": "SUB"},
        )

    @_("get_index EQ_SUB expression ';'")
    def variable_operation(self, p):
        return (
            "VARIABLE_OPERATION",
            {"ID": p.get_index, "EXPRESSION": p.expression, "OPERATION": "SUB"},
        )

    @_("ID EQ_MUL expression ';'")
    def variable_operation(self, p):
        return (
            "VARIABLE_OPERATION",
            {"ID": p.ID, "EXPRESSION": p.expression, "OPERATION": "MUL"},
        )

    @_("get_index EQ_MUL expression ';'")
    def variable_operation(self, p):
        return (
            "VARIABLE_OPERATION",
            {"ID": p.get_index, "EXPRESSION": p.expression, "OPERATION": "MUL"},
        )

    @_("ID EQ_MOD expression ';'")
    def variable_operation(self, p):
        return (
            "VARIABLE_OPERATION",
            {"ID": p.ID, "EXPRESSION": p.expression, "OPERATION": "MOD"},
        )

    @_("get_index EQ_MOD expression ';'")
    def variable_operation(self, p):
        return (
            "VARIABLE_OPERATION",
            {"ID": p.get_index, "EXPRESSION": p.expression, "OPERATION": "MOD"},
        )

    @_("ID EQ_DIV expression ';'")
    def variable_operation(self, p):
        return (
            "VARIABLE_OPERATION",
            {"ID": p.ID, "EXPRESSION": p.expression, "OPERATION": "DIV"},
        )

    @_("get_index EQ_DIV expression ';'")
    def variable_operation(self, p):
        return (
            "VARIABLE_OPERATION",
            {"ID": p.get_index, "EXPRESSION": p.expression, "OPERATION": "DIV"},
        )

    @_("class_attribute '=' expression ';'")
    def class_attribute_assignment(self, p):
        return (
            "CLASS_ATTRIBUTE_ASSIGNMENT",
            {"CLASS_ATTRIBUTE": p.class_attribute, "EXPRESSION": p.expression},
        )

    @_("if_statement")
    def conditional(self, p):
        return (
            "CONDITIONAL",
            {"IF": p.if_statement, "ELSE_IF": (None, None), "ELSE": (None, None)},
        )

    @_("if_statement else_if_loop")
    def conditional(self, p):
        return (
            "CONDITIONAL",
            {"IF": p.if_statement, "ELSE_IF": p.else_if_loop, "ELSE": (None, None)},
        )

    @_("if_statement else_if_loop else_statement")
    def conditional(self, p):
        return (
            "CONDITIONAL",
            {"IF": p.if_statement, "ELSE_IF": p.else_if_loop, "ELSE": p.else_statement},
        )

    @_("if_statement else_statement")
    def conditional(self, p):
        return (
            "CONDITIONAL",
            {"IF": p.if_statement, "ELSE_IF": (None, None), "ELSE": p.else_statement},
        )

    @_("IF '(' expression ')' '{' program '}'")
    def if_statement(self, p):
        return ("IF", {"CODE": p.program, "CONDITION": p.expression})

    @_("else_if_loop else_if_statement")
    def else_if_loop(self, p):
        return p.else_if_loop + (p.else_if_statement,)

    @_("else_if_statement")
    def else_if_loop(self, p):
        return ("ELSE_IF", p.else_if_statement)

    @_("ELSE IF '(' expression ')' '{' program '}'")
    def else_if_statement(self, p):
        return ({"CODE": p.program, "CONDITION": p.expression},)

    @_("ELSE '{' program '}'")
    def else_statement(self, p):
        return ("ELSE", {"CODE": p.program})

    @_("DEL ID ';'")
    def delete_statement(self, p):
        return ("DEL", {"ID": p.ID})

    @_("IMPORT expression ';'")
    def import_statement(self, p):
        return ("IMPORT", {"EXPRESSION": p.expression})

    # Statment syntax END
    ###########################################################################
    # Expression START

    @_("'-' expression %prec UMINUS")
    def expression(self, p):
        return ("NEG", p.expression)

    @_("'+' expression %prec UPLUS")
    def expression(self, p):
        return ("POS", p.expression)

    @_("expression '+' expression")
    def expression(self, p):
        return ("ADD", p[0], p[2])

    @_("expression '-' expression")
    def expression(self, p):
        return ("SUB", p[0], p[2])

    @_("expression '/' expression")
    def expression(self, p):
        return ("DIV", p[0], p[2])

    @_("expression '*' expression")
    def expression(self, p):
        return ("MUL", p[0], p[2])

    @_("expression '%' expression")
    def expression(self, p):
        return ("MOD", p[0], p[2])

    @_("expression EQEQ expression")
    def expression(self, p):
        return ("EQEQ", p[0], p[2])

    @_("expression NOT_EQEQ expression")
    def expression(self, p):
        return ("NOT_EQEQ", p[0], p[2])

    @_("expression EQ_LESS expression")
    def expression(self, p):
        return ("EQ_LESS", p[0], p[2])

    @_("expression EQ_GREATER expression")
    def expression(self, p):
        return ("EQ_GREATER", p[0], p[2])

    @_("expression '|' expression")
    def expression(self, p):
        return ("OR", p[0], p[2])

    @_("expression '&' expression")
    def expression(self, p):
        return ("AND", p[0], p[2])

    @_("'!' expression")
    def expression(self, p):
        return ("NOT", p.expression)

    @_("expression '<' expression")
    def expression(self, p):
        return ("LESS", p[0], p[2])

    @_("expression '>' expression")
    def expression(self, p):
        return ("GREATER", p[0], p[2])

    @_("'(' expression ')'")
    def expression(self, p):
        return p.expression

    @_("python_code")
    def expression(self, p):
        return p.python_code

    @_("function_call")
    def expression(self, p):
        return p.function_call

    @_("get_index")
    def expression(self, p):
        return p.get_index

    @_("null")
    def expression(self, p):
        return p.null

    @_("int")
    def expression(self, p):
        return p.int

    @_("float")
    def expression(self, p):
        return p.float

    @_("bool")
    def expression(self, p):
        return p.bool

    @_("string")
    def expression(self, p):
        return p.string

    @_("id")
    def expression(self, p):
        return p.id

    @_("class_attribute")
    def expression(self, p):
        return p.class_attribute

    @_("_tuple")
    def expression(self, p):
        return p._tuple

    @_("_list")
    def expression(self, p):
        return p._list

    @_("_numpy")
    def expression(self, p):
        return p._numpy

    # Expression END
    ###########################################################################
    # Intermediate expression START

    @_("NULL")
    def null(self, p):
        return ("NULL", "NULL")

    @_("expression '[' expression ']'")
    def get_index(self, p):
        return ("GET_INDEX", {"EXPRESSION": p.expression0, "INDEX": p.expression1})

    @_("'{' positional_args '}'")
    def _tuple(self, p):
        return ("TUPLE", {"ITEMS": p.positional_args})

    @_("'[' positional_args ']'")
    def _list(self, p):
        return ("LIST", {"ITEMS": p.positional_args})

    @_("'(' positional_args ')'")
    def _numpy(self, p):
        return ("NUMPY", {"ITEMS": p.positional_args})

    @_("INT")
    def int(self, p):
        return ("INT", {"VALUE": p.INT})

    @_("STRING")
    def string(self, p):
        return ("STRING", {"VALUE": p.STRING[1:-1]})

    @_("FLOAT")
    def float(self, p):
        return ("FLOAT", {"VALUE": p.FLOAT})

    @_("TRUE")
    def bool(self, p):
        return ("BOOL", {"VALUE": p.TRUE})

    @_("FALSE")
    def bool(self, p):
        return ("BOOL", {"VALUE": p.FALSE})

    @_("expression COLON_COLON ID")
    def class_attribute(self, p):
        return ("CLASS_ATTRIBUTE", {"CLASS": p[0], "ATTRIBUTE": p[2]})

    @_("ID")
    def id(self, p):
        return ("ID", {"VALUE": p.ID})

    @_("PYTHON_CODE")
    def python_code(self, p):
        return ("PYTHON_CODE", {"CODE": p.PYTHON_CODE[1:-1]})

    @_("%prec EMPTY")
    def empty(self, p):
        pass

    # Intermediate expression END
    ###########################################################################
    # Syntax error START
