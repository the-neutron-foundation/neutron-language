try:
    import neutron.neutron_lexer as neutron_lexer
    import neutron.neutron_parser as neutron_parser
    import neutron.neutron_interpreter as neutron_interpreter
except ModuleNotFoundError:
    import neutron_lexer as neutron_lexer
    import neutron_parser as neutron_parser
    import neutron_interpreter as neutron_interpreter
import pprint
from os import path
import logging
from copy import deepcopy


def read_file(filename):
    file_ = open(path.abspath(filename), "r")
    file_contents = file_.read()
    file_.close()
    return file_contents


def get_objects(filename):
    text = read_file(filename)
    lexer = neutron_lexer.NeutronLexer()
    parser = neutron_parser.NeutronParser()
    tree = parser.parse(lexer.tokenize(text))
    program = neutron_interpreter.Process(tree, filename=path.abspath(filename), imported=True)
    program.run()
    return (deepcopy(program.objects), deepcopy(neutron_interpreter.global_objects))


def main(filename, verbose=False):
    text = read_file(filename)
    defult_functions = get_objects(
        path.join(path.dirname(path.abspath(__file__)), "defult.ntn")
    )
    pp = pprint.PrettyPrinter(indent=2)
    lexer = neutron_lexer.NeutronLexer()
    parser = neutron_parser.NeutronParser()
    if verbose:
        for tok in lexer.tokenize(text):
            print(tok)
    tree = parser.parse(lexer.tokenize(text))
    if verbose:
        pp.pprint(tree)
    program = neutron_interpreter.Process(tree, filename=path.abspath(filename))
    program.objects.update(defult_functions[0])
    neutron_interpreter.global_objects.update(defult_functions[1])
    program.run()
