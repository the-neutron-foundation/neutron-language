import neutron_interpreter, neutron_parser, neutron_lexer
import pprint
from os import path


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
    return (program.objects, program.class_templates, neutron_interpreter.global_objects, neutron_interpreter.global_class_templates)

def main(filename, if_return=True):
    text = read_file(filename)
    defult_functions = get_objects(path.join(path.dirname(path.abspath(__file__)), "defult.ntn"))
    pp = pprint.PrettyPrinter(indent=2)
    lexer = neutron_lexer.NeutronLexer()
    parser = neutron_parser.NeutronParser()
    for tok in lexer.tokenize(text):
        print(tok)
    tree = parser.parse(lexer.tokenize(text))
    pp.pprint(tree)
    program = neutron_interpreter.Process(tree, filename=path.abspath(filename))
    program.objects["--file--"] = path.abspath(filename)
    neutron_interpreter.global_objects["--file--"] = path.abspath(filename)
    program.objects.update(defult_functions[0])
    program.class_templates.update(defult_functions[1])
    neutron_interpreter.global_objects.update(defult_functions[2])
    neutron_interpreter.global_class_templates.update(defult_functions[3])
    program.run()
    return (program, neutron_interpreter.global_objects, neutron_interpreter.global_class_templates) if if_return else None


if __name__ == '__main__':
    main("test.ntn")
