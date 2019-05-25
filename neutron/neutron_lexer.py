from sly import Lexer


class NeutronLexer(Lexer):

    tokens = {ID, FLOAT, INT, FUNC, CLASS, STRING, EQ_GREATER, EQ_LESS, EQEQ, PYTHON_CODE, COLON_COLON, KWORD, IF, ELSE, TRUE, FALSE, NOT_EQEQ}
    literals = { "+", "-", "*", "/", "%", "|", "&", "!", ">", "<", "=", "(", ")", "{", "}", ";", ",", ":"}

    ignore = " \t"
    ignore_comment_slash = r"//.*"

    FLOAT = r"\d*\.\d+"
    INT = r"\d+"

    PYTHON_CODE = r"`[.\W\w]*?`"
    STRING = r"\".*?(?<!\\)(\\\\)*\""
    ID = r"(--[a-zA-Z_]([a-zA-Z0-9_]|!)*--|[a-zA-Z_]([a-zA-Z0-9_]|!)*)"
    ID["func"] = FUNC
    ID["class"] = CLASS
    ID["kword"] = KWORD
    ID["true"] = TRUE
    ID["false"] = FALSE
    ID["if"] = IF
    ID["else"] = ELSE

    COLON_COLON = r"::"
    EQEQ = r"=="
    NOT_EQEQ = r"!="
    EQ_GREATER = r"=>"
    EQ_LESS = r"=<"


    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += len(t.value)

if __name__ == '__main__':
    data = '''# Counting
boolthing = -1239283.132 / +123132.23 == +12317.324 / 24873847823784784;
pfunc (hi) {
    code = "print(hi)";
    pcode code;
}
'''
    lexer = NeutronLexer()
    for tok in lexer.tokenize(data):
        print(tok)
