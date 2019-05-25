class Foo:
    def __init__(self, arg1):
        self.arg1 = arg1

def main(class_obj):
    # Returns false and is type <class 'file1.Foo'>
    print(type(class_obj))
    print(isinstance(class_obj, Foo))

    # Returns true and is type <class '__main__.Foo'>
    foo_local = Foo("argument")  # Class initiated in __main__ seems to work
    print(type(foo_local))
    print(isinstance(foo_local, Foo))

from file2 import get_class
main(get_class())
