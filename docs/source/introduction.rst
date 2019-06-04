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
``IntType``
***************
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

Other types
^^^^^^^^^^^
``StringType``
**************
This type implements the python 3 ``str`` class. You can concatenate strings in neutron in the same way as python.

.. code-block:: java

  "Hello, " + "World!"; // Evaluates to "Hello, World"

.. warning::
  Types cannot mix (e.g. ``IntType`` and ``FloatType``, or ``StringType`` and ``BoolType``)

``NumpyArray``
**************
This type is the same as the Numpy ``array()`` class. This is built in and ever object in the array is separated by commas. all of that is around a pair of square brackets.

.. code-block:: java

  [1, 2, 3, 4, 5];  // Evaluates to Numpy Array

``ListType``
************

``TupleType``
*************

Variable Assignment
^^^^^^^^^^^^^^^^^^^

Function
^^^^^^^^

Function Definition
*******************

Function Call
*************

Classes
^^^^^^^

Defining a Class
****************

Making Instance of Class
************************

Running Methods
***************
