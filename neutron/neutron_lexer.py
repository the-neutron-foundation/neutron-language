from sly import Lexer


class NeutronLexer(Lexer):

    tokens = {
        ID,
        FLOAT,
        INT,
        FUNC,
        CLASS,
        STRING,
        EQ_GREATER,
        EQ_LESS,
        EQEQ,
        PYTHON_CODE,
        COLON_COLON,
        IF,
        ELSE,
        TRUE,
        FALSE,
        NOT_EQEQ,
        WHILE,
        BREAK,
        FOR,
        IN,
        DEL,
        RETURN,
        NULL,
        EQ_ADD,
        EQ_SUB,
        EQ_MUL,
        EQ_DIV,
        EQ_MOD,
        IMPORT,
    }
    literals = {
        "+",
        "-",
        "*",
        "/",
        "%",
        "|",
        "&",
        "!",
        ">",
        "<",
        "=",
        "(",
        ")",
        "{",
        "}",
        ";",
        ",",
        ":",
        "[",
        "]",
    }

    ignore = " \t"
    ignore_comment_slash = r"//.*"

    FLOAT = r"\d*\.\d+"
    INT = r"\d+"

    PYTHON_CODE = r"`[.\W\w]*?`"
    STRING = r"(\".*?(?<!\\)(\\\\)*\"|'.*?(?<!\\)(\\\\)*')"
    ID = r"(--[a-zA-Z_]([a-zA-Z0-9_]|!)*--|[a-zA-Z_]([a-zA-Z0-9_]|!)*)"
    ID["func"] = FUNC
    ID["class"] = CLASS
    ID["break"] = BREAK
    ID["true"] = TRUE
    ID["false"] = FALSE
    ID["while"] = WHILE
    ID["for"] = FOR
    ID["in"] = IN
    ID["if"] = IF
    ID["else"] = ELSE
    ID["del"] = DEL
    ID["null"] = NULL
    ID["return"] = RETURN
    ID["import"] = IMPORT

    COLON_COLON = r"::"
    EQEQ = r"=="
    NOT_EQEQ = r"!="
    EQ_GREATER = r"=>"
    EQ_LESS = r"=<"
    EQ_ADD = r"\+="
    EQ_SUB = r"-="
    EQ_MUL = r"\*="
    EQ_DIV = r"/="
    EQ_MOD = r"%="

    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += len(t.value)
