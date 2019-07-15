Primitive Types
===============
Note that with the examples below, the code won't actually work, because neutron doesn't understand single expression by themselves.

``IntType``
-----------
This type implement the python 3 ``int`` class. It can only include whole numbers (not decimals). If you divide integers, if results in a decimal, it rounds down. Note adding an integer to an integer returns an integer.
Here is an example:

.. code-block:: neutron

  1 + 1; // Evaluates to 2
  3 / 2; // Evaluates to 1 (round down)
  2 * 3; // Evaluates to 6
  20 - 3; // Evaluates to 17
  3 + 2.1; // Error can't add int to float

``FloatType``
-------------
This type implement the python 3 ``float`` class. It can decimals and whole numbers. Note it must contain a decimal (i.e ``1.00``). Adding a float to a float returns a float.
Example:

.. code-block:: neutron

  1.0 + 1.2; // Evaluates to 2.2
  3.0 / 2.0; // Evaluates to 1.5
  2.2 * 3.7; // Evaluates to 8.14
  20.0 - 3.2; // Evaluates to 16.8
  3.5 + 2; // Error can't add int to float

``StringType``
--------------
This type implements the python 3 ``str`` class. You can concatenate strings in neutron in the same way as python.

.. code-block:: neutron

  "Hello, " + "World!"; // Evaluates to "Hello, World"

``BoolType``
------------
This type implements the python 3 ``bool`` class.

.. code-block:: neutron

  true; // Evaluates to true
  false; // Evaluates to false

.. warning::
  Types cannot mix (e.g. adding ``IntType`` and ``FloatType``, or adding ``StringType`` and ``BoolType``)
