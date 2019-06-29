Customization
=============

Putting Python Code
^^^^^^^^^^^^^^^^^^^
It is possible to make functions that have python functionality by putting inline python code. This is how the ``io`` packages were written.

To put inline python code into your Neutron code, use the backtick `````. **Note that shown here, there are 2 backticks, but there should be 1, but Sphinx does not render a single backtick properly.** You can use python code anywhere as an expression, or just pure python code.

Example of pure inline python code:

.. code-block:: python

  ``print("Hello, Neutron!")
  x = "how are you?"
  a_python_function_here()``;

Example of python code being used as an expression:

.. code-block:: java

  a_neutron_function(`python_function(10), `20`, 30); // Use python code as positional arguments
  x = `len("Hello World!")`; // len is 12

In order to get variables, or make them, your must do it in a special way. To make a variable, use the namespace ``var`` for local variables and ``gvar`` for global variables. Example:

.. code-block:: python

  ``var.local_variable = "foo"
  gvar.global_variable = "This is a global variable"``;

To reference to a variable, just use the namespace ``var`` for local variables and ``gvar`` for global variables, and don't assign them to anything. Example:

.. code-block:: python

  ``var.local_variable # get value of variable
  gvar.global_variable``;

Making Types
^^^^^^^^^^^^
To make a variable, you cannot just simply assign a variable. You must make the appropriate class for the appropriate type you are assigning a variable to. For example, to make an integer 10, you must use the ``bt.IntType`` and use the python ``10``, and make the ``enter_value`` keyword argument ``True``. Example:

.. code-block:: python

  ``var.foo = bt.IntType(10, enter_value=True)
  var.foo = bt.StringType("this is a string", enter_value=True)
  var.foo = bt.NumpyArray(np.array(1, 2, 3, 4), enter_value=True)``;

Note that in this case, ``bt`` is short for builtin types.

The builtin type available are:

``bt.IntType`` - for integers

``bt.FloatType`` - for floats

``bt.StringType`` - for strings

``bt.BoolType`` - for booleans

``bt.NumpyArray`` - for Numpy arrays

``bt.ListType`` - for python-like lists

``bt.TupleType`` - for python-like tuples
