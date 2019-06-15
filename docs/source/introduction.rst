Introduction
============

Installation
------------
To use, either install the binaries (find them `here <https://github.com/the-neutron-foundation/neutron/releases>`_), build them yourself, or directly run (using the default CPython interpreter) the python 3 code (slower). If you choose to build it yourself, you should have `Numpy <https://www.numpy.org/>`_ installed. Neutron uses a python 3 compiler called `Nuitka <https://nuitka.net/pages/overview.html>`_, which is faster.
To compile from source, get `Nuitka <https://nuitka.net/pages/overview.html>`_.
After that, go to the source folder (the master folder) there should be a ``neutron`` folder in the master folder, and run the Nuitka build commands. Here are the commands (run in order):

.. code-block:: bash

 $ pip3 install nuitka  # install nuitka

 $ git clone https://github.com/the-neutron-foundation/neutron  # get repo

 $ cd neutron

 $ python3 -m nuitka --follow-imports --include-plugin-directory=./neutron --show-progress --show-scons neutron # compile neutron using python -m flag

After compiling, you should see a ``neutron.exe`` file and a ``neutron.bin`` file. These are your binaries. To use the .bin binaries on Unix systems just run ``./neutron.bin``. On windows, the ``.exe`` file can just be run as ``neutron`` in the command prompt.


Usage
-----
Running a file
^^^^^^^^^^^^^^
To use neutron, pass the filename as the first argument to the neutron binary if you built it from source.

.. code-block:: bash

 ./neutron path/to/neutron/file.ntn

If you plan to just run the normal source code, just pass neutron as the package and the normal arguments after. Make sure you are in the main directory, and not in the `neutron-repo/neutron` path. Example:

.. code-block:: bash

 python3 neutron path/to/neutron/file.ntn

Optional Flags
^^^^^^^^^^^^^^
Verbose
*******
Option: ``--verbose`` or ``-v``

Info: make neutron print out the parse tree and the tokens and general debug info.

Example: ``neutron file.ntn -v``

Writing Neutron
---------------
Commenting
^^^^^^^^^^
For now, there are only single line comments. All single line comments start with a ``//``. For example:

.. code-block:: java

  code_here; // This is a comment

Primitive Types
^^^^^^^^^^^^^^^
Note that with the examples below, the code won't actually work, because neutron doesn't understand single expression by themselves.

``IntType``
***********
This type implement the python 3 ``int`` class. It can only include whole numbers (not decimals). If you divide integers, if results in a decimal, it rounds down. Note adding an integer to an integer returns an integer.
Here is an example:

.. code-block:: java

  1 + 1; // Evaluates to 2
  3 / 2; // Evaluates to 1 (round down)
  2 * 3; // Evaluates to 6
  20 - 3; // Evaluates to 17
  3 + 2.1; // Error can't add int to float

``FloatType``
*************
This type implement the python 3 ``float`` class. It can decimals and whole numbers. Note it must contain a decimal (i.e ``1.00``). Adding a float to a float returns a float.
Example:

.. code-block:: java

  1.0 + 1.2; // Evaluates to 2.2
  3.0 / 2.0; // Evaluates to 1.5
  2.2 * 3.7; // Evaluates to 8.14
  20.0 - 3.2; // Evaluates to 16.8
  3.5 + 2; // Error can't add int to float

``StringType``
**************
This type implements the python 3 ``str`` class. You can concatenate strings in neutron in the same way as python.

.. code-block:: java

  "Hello, " + "World!"; // Evaluates to "Hello, World"

``BoolType``
**************
This type implements the python 3 ``bool`` class.

.. code-block:: java

  true; // Evaluates to true
  false; // Evaluates to false

.. warning::
  Types cannot mix (e.g. adding ``IntType`` and ``FloatType``, or adding ``StringType`` and ``BoolType``)

Other types
^^^^^^^^^^^

``NumpyArray``
**************
This type is the same as the Numpy ``array()`` class. This is built in and every object in the array is separated by commas. All of that is around a pair of brackets.

.. code-block:: java

  (1, 2, 3, 4, 5);  // Evaluates to Numpy Array

``ListType``
************
This type is the same as the Python list class. This is built in and every object in the array is separated by commas. All of that is around a pair of square brackets.

.. code-block:: java

  [1, 2, 3, 4, 5];  // Evaluates to python list Array

``TupleType``
*************
This type is the same as the Python tuple class. This is built in and every object in the array is separated by commas. All of that is around a pair of curly brackets.

.. code-block:: java

  {1, 2, 3, 4, 5};  // Evaluates to python tuple Array

Variables
^^^^^^^^^
Variables in Neutron are simple and elegant to use, like in python. You do not need to define the type the the variable is.

Variable Assignment
*******************
To declare a variable in the local scope, put the name of the variable, an equals sign, and the value of the variable, and a semi-colon, of-course. Example:

.. code-block:: java

  variable_here = 102;  // Make variable with name "variable_here" and value 102

Getting Variable Value
**********************
To get the value of a variable, just type in the name of the variable. Example:

.. code-block:: java

  hello = "Hello, World";  // Make variable with name "hello" and value "Hello, World"
  hello;  // Evaluates to "Hello, World"

Functions
^^^^^^^^^
Functions in neutron are also implemented. In Neutron, there are keyword arguments and positional arguments.

Function Definition
*******************
There are many things to know when defining functions. The syntax for defining arguments are similar to that of python. The positional arguments are followed by the keyword arguments.
The ``func`` keyword is used to define functions. This is followed by the name of the function, then in brackets the positional and keyword arguments. Not that a function does not have to have positional or keyword arguments.
Example:

.. code-block:: java

  func this_is_a_function(positional_argument, arg2, blah, foo, keyword_argument=10, foo=2313, bar="sadjis") {
    // Do code here
  }

To make a function return something, set the special variable ``--return--``. This tells the Neutron interpreter that when this function is called, and returns this value. Example:

.. code-block:: java

  func get_sum(arg1, arg2) {
    --return-- = arg1 + arg2;  // Return sum of two arguments
  }

  x = get_sum(1, 2)  // variable "x" now has the value "3"

Function Call
*************
To call a function, brackets must be put around the arguments. Example:

.. code-block:: java

  function_example("Hello, World", "blah");  // Run function "function_example" with arguments "Hello, World" and "blah"
  function2(23, optional_arg=203, foo=23);  // Specify keyword arguemts

A variable or anything, for that matter, may be assigned as a function (yes, the object, not just the return value). For example:

.. code-block:: java

  x = function_example(10);
  y = function_example;
  x_new = y(10);  // same as "x"

Classes
^^^^^^^
Classes in Neutron are very similar to those in python. Right now, there are magic methods, like python. Here is a list of python-like magic methods:

- ``--init--`` - is run when an instance of the class is made

They are an object, and any function defined in the class will be defined. Classes are used through methods, which are really just functions defined in a class.

Defining a Class
****************
To make a class, use the ``class`` keyword, and provide the name of the class after. Inside the class, define functions that you want to make into methods. Note that instead of ``self``, like in python, the ``this`` argument should be used, in fact, if you don't use the the ``this`` argument as your first argument, the neutron interpreter will complain. Example:

.. code-block:: java

  class MyClass {
    func --init--(this, foo) {
      this::foo = 10;
      this::numpy_array = (230, 34, 23);
    }
    func return_numpy_array(this) {
      --return-- = this::numpy_array;
    }
  }

Note that you can also use the special variable ``--return--`` in a method.

Making Instance of Class
************************
To make an instance of a class, simply just call the class like a function, and provide the arguments needed by the ``--init--`` method. Note that the ``this`` argument is passed by the neutron interpreter. For example:

.. code-block:: java

  class MyClass {
    func --init--(this, _foo) {  // Don't pollute variables
      this::foo = _foo;
      this::numpy_array = (230, 34, 23);
    }
    func return_numpy_array(this) {
      --return-- = this::numpy_array;
    }
  }

  instance_of_my_class = MyClass(123);  // Make instance of MyClass

Now, ``instance_of_my_class`` is an instance of the ``MyClass`` class.

Running Methods
***************
To run a method, simply use double colons and a pair of parentheses. Note that you also don't need to provide the ``this`` argument either, because the neutron interpreter does it for you. Example:

.. code-block:: java

  instance_of_my_class = MyClass(123);  // Make instance of MyClass
  my_array = instance_of_my_class::return_numpy_array();  // Run return_numpy_array method on MyClass

Getting and Setting Attributes
******************************
To set and get attributes, simply just assign values using a single equals sign. Example:

.. code-block:: java

  instance_of_my_class::array = [12, 45, 23, 42, 87];  // Redefine array attribute in instance_of_my_class
  x = instance_of_my_class::foo;  // Assign x to the value of instance_of_my_class's attribute foo

Conditionals
^^^^^^^^^^^^
Conditionals work around the same in python.

If
****
If statements use the ``if`` keyword, followed by the condition in parentheses, followed by the code to run. Example:

.. code-block:: java

  if (true) {
    // run code here
  }

Else If
*******
Else if statements use the ``else`` and ``if`` keyword, followed by the condition in parentheses, followed by the code to run. They go after if statements and are run if the previous if statement evaluated to ``false``. Note the python ``elif`` keyowrd does not work. Example:

.. code-block:: java

  if (false) {
    // code that won't run
  } else if (true) {
    // run code here
  }

Else
****
Else if statements also go after if or else if statements, and are run when everything before it evaluated to false. They do not need a condition and use the ``else`` keyword. Example:

.. code-block:: java

  if (false) {
    // code that won't run
  } else if (false) {
    // code that won't run
  } else {
    // code that will run
  }

Operators
^^^^^^^^^
There are many operators on different types in neutron. You can use parentheses for grouping.

Math
****
Note that with math, order of operations is applied.


**``+``** - add two values together

**``-``** - subtract two values

**``/``** - divide first value by second value

**``\*``** - multiply two values together

**``%``** - get remainder of division (modulo operation)


Logic
*****

The order of which logic operations are applied are: ``!``, ``&``, ``|``

**``!``** - NOT operation: return true if false and false if true

**``&``** - AND operation: return true if both values are true otherwise return false

**``|``** - OR operation: return true if both values or one value is true, otherwise false


While Loops
^^^^^^^^^^^
While loops are like while loops in python. They keep on looping until a certain condition is false. This condition is put in parentheses and the code that is to be run is but in curly braces. Example:

.. code-block:: java

  x = 0;  // Declare variable x
  while (x < 10) {  // Check if x is greater than 10, if so, break out of loop
    x += 1;
  }
  // now x == 10

Built-In Functions
^^^^^^^^^^^^^^^^^^
There are many builtin functions that are the building blocks of Neutron.

``get!``
********
The ``get!`` function is how you import packages into you neutron file. The first argument is the path to the file youare trying to import. When looking for the file, neutron looks in the system directory first, then the relative path of the neutron file that is being run. You can do ``get!("io")`` to get the entire ``io`` package namespaced (that is, without the ``io::`` needed), or you can get individual files (e.g. ``get!("io/print")``).

``io``
******
The ``io`` package deals with the input/output of the program.

``io/print``
""""""""""""
``io/print`` prints the raw value of the argument passed.

``io/print_type``
"""""""""""""""""
``io/print_type`` prints the type of the argument given and some extra info.

``io/stdin``
""""""""""""
``io/stdin`` gets user input and is similar to the python ``input`` function. It takes an optional keyword argument called ``prompt``. The prompt is printed out. After the user presses enter, the value will be returned.

``types``
*********
This package is responsible for the conversion of types.

``types/to_int``
""""""""""""""""
``types/to_int`` converts any given type to ``IntType``. (``FloatType``, ``StringType``, etc.)
