import neutron.neutron_lexer as neutron_lexer
import neutron.neutron_parser as neutron_parser
import neutron.neutron_interpreter as neutron_interpreter
import pprint
from os import path
import logging


def read_file(filename):
    file_ = open(filename, "r")
    file_contents = file_.read()
    file_.close()
    return file_contents


def get_objects(filename):
    text = read_file(filename)
    lexer = neutron_lexer.NeutronLexer()
    parser = neutron_parser.NeutronParser()
    tree = parser.parse(lexer.tokenize(text))
    program = neutron_interpreter.Process(tree, filename=path.abspath(filename))
    program.run()
    return (program.objects, neutron_interpreter.global_objects)

def main(filename, if_return=True, verbose=False):
    text = read_file(filename)
    defult_functions = get_objects(path.join(path.dirname(path.abspath(__file__)), "defult.ntn"))
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
    program.objects["--file--"] = path.abspath(filename)
    neutron_interpreter.global_objects["--file--"] = path.abspath(filename)
    program.objects.update(defult_functions[0])
    neutron_interpreter.global_objects.update(defult_functions[1])
    program.run()
    return (program, neutron_interpreter.global_objects) if if_return else None
