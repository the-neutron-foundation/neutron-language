Functions
=========
Functions in neutron are also implemented. In Neutron, there are keyword arguments and positional arguments.

Function Definition
-------------------
There are many things to know when defining functions. The syntax for defining arguments are similar to that of python. The positional arguments are followed by the keyword arguments.
The ``func`` keyword is used to define functions. This is followed by the name of the function, then in brackets the positional and keyword arguments. Not that a function does not have to have positional or keyword arguments.
Example:

.. code-block:: neutron

  func this_is_a_function(positional_argument, arg2, blah, foo, keyword_argument=10, foo=2313, bar="sadjis") {
    // Do code here
  }

To make a function return something, set the special variable ``--return--``, or use the return keyword. This tells the Neutron interpreter that when this function is called, it should return the value assigned to ``--return--``, or whatever is after the return statement.
Note that the ``return`` statement quits out of the function and assigning the ``--return--`` doesn't. If no return value is assigned, the ``NullType`` value will be returned.
Example:

.. code-block:: neutron

  func get_sum(arg1, arg2) {
    --return-- = arg1 + arg2;  // Return sum of two arguments
    // Code here runs
  }
  func get_diff(arg1, arg2) {
    return arg1 - arg2;  // Return sum of two arguments
    // Code here doesn't run
  }

  x = get_sum(1, 2)  // variable "x" now has the value "3"

Function Call
-------------
To call a function, brackets must be put around the arguments. Example:

.. code-block:: neutron

  function_example("Hello, World", "blah");  // Run function "function_example" with arguments "Hello, World" and "blah"
  function2(23, optional_arg=203, foo=23);  // Specify keyword arguemts

A variable or anything, for that matter, may be assigned as a function (yes, the object, not just the return value). For example:

.. code-block:: neutron

  x = function_example(10);
  y = function_example;
  x_new = y(10);  // same as "x"
