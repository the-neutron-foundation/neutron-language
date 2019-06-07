Introduction
============

Installation
------------
To use, either install the binaries (find them `here <https://github.com/the-neutron-foundation/neutron/releases>`_), or build them yourself. If you choose to build it yourself, you should have `Numpy <https://www.numpy.org/>`_ installed. Neutron uses a python 3 compiler called `Nuitka <https://nuitka.net/pages/overview.html>`_, which is faster.
Note that running neutron with the defult python implantation (CPython) won't work, because the import system works differently. To compile from source, get `Nuitka <https://nuitka.net/pages/overview.html>`_.
After that, go to the source folder (the master folder) there should be a ``neutron`` folder in the master folder, and run the Nuitka build commands. Here are the commands (run in order):

.. code-block:: bash

 $ pip3 install nuitka  # install nuitka

 $ git clone https://github.com/the-neutron-foundation/neutron  # get repo

 $ cd neutron

 $ python3 -m nuitka --follow-imports --include-plugin-directory=./neutron --show-progress --show-scons neutron # compile neutron using python -m flag

After compilling, you should see a ``neutron.exe`` file and a ``neutron.bin`` file. These are your binaries. To use the .bin binaries on Unix systems just run ``./neutron.bin``. On windows, the ``.exe`` file can just be run as ``neutron`` in the command prompt.


Usage
-----
Running a file
^^^^^^^^^^^^^^
To use neutron, pass the filename as the first argument to the neutron binary.

.. code-block:: bash

 ./neutron path/to/neutron/file.ntn

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
This type implement the python 3 ``float`` class. It can decimals and whole numbers. Note it must contain a decimal (i.e ``1.00``). Note adding a float to a float returns a float.
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

Defining a Class
****************

Making Instance of Class
************************

Running Methods
***************

Conditionals
^^^^^^^^^^^^

If
****

Else If
*******

Else
****

Operators
^^^^^^^^^

Math
****

Boolean
*******

Built-In Functions
^^^^^^^^^^^^^^^^^^

While Loops
^^^^^^^^^^^
