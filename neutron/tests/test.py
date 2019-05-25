from os import path
from chain import main

path_of_file = self.objects["path_of_file"]
os_path = path.join(paths_to_look_in[0], path.dirname(path_of_file))
file_name = path.abspath(os_path + ".cn")
if file_name.isfile():
    program = main(file_name)
    global_class_templates.update(program[2])
    global_objects.update(program[1])
elif os_path.isdir():
    file_name = path.join(os_path + "--init--.cn")
    program = main(file_name)
    global_class_templates.update(program[2])
    global_objects.update(program[1])
