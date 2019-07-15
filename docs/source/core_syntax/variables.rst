Variables
=========
Variables in Neutron are simple and elegant to use, like in python. You do not need to define the type the the variable is.

Variable Assignment
-------------------
To declare a variable in the local scope, put the name of the variable, an equals sign, and the value of the variable, and a semi-colon, of-course. Example:

.. code-block:: neutron

  variable_here = 102;  // Make variable with name "variable_here" and value 102

Getting Variable Value
----------------------
To get the value of a variable, just type in the name of the variable. Example:

.. code-block:: neutron

  hello = "Hello, World";  // Make variable with name "hello" and value "Hello, World"
  hello;  // Evaluates to "Hello, World"

Assignment Operators
--------------------
You can add, subtract, multiply, divide, or modulo a variable, with out using the ``x = x + 1;`` idiom. You use the ``+=``, ``-=``, ``*=``, ``/=``, and ``%=`` operator. For example:

.. code-block:: neutron

  x = 1;
  x += 1000; // x is now 1001
  x -= 1000; // x is now 1 again
  x *= 3; // x is now 3
  x /= 2; // x is now 1 (integer division)
  y = 13;
  y %= 10; // y is now 3 (because 13 % 10 is 3)
