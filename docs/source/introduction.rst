Introduction
============

Dependencies
------------
Before installing/building/running neutron, you should first install the dependencies. you can do this via `pip3` or any other package manager. The dependencies required are:

- `Numpy <https://www.numpy.org/>`_
- `SLY <https://github.com/dabeaz/sly>`_

Installation
------------
To use, either install the binaries (find them `here <https://github.com/the-neutron-foundation/neutron/releases>`_), build them yourself, or directly run the python 3 code using `CPython <https://www.python.org/downloads/>`_ (slow) or `PyPy <https://pypy.org/>`_ (very fast). It is recommended to use `PyPy <https://pypy.org/>`_, for its speed. If you choose to build it yourself, you should have `Numpy <https://www.numpy.org/>`_ installed. Neutron can also be compiled using a python 3 compiler called `Nuitka <https://nuitka.net/pages/overview.html>`_. **It is recommended to use pypy for its speed**.
To compile from source, get `Nuitka <https://nuitka.net/pages/overview.html>`_.
After that, go to the source folder (the master folder) there should be a ``neutron`` folder in the master folder, and run the Nuitka build commands. Here are the commands (run in order):

.. code-block:: bash

 $ pip3 install numpy  # install numpy

 $ pip3 install sly  # install sly

 $ pip3 install nuitka  # install nuitka

 $ git clone https://github.com/the-neutron-foundation/neutron  # get repo

 $ cd neutron

 $ python3 -m nuitka --follow-imports --include-plugin-directory=./neutron --show-progress --show-scons neutron # compile neutron using python -m flag

After compiling, you should see a ``neutron.exe`` file and a ``neutron.bin`` file. These are your binaries. To use the .bin binaries on Unix systems just run ``./neutron.bin``. On windows, the ``.exe`` file can just be run as ``neutron`` in the command prompt.


Usage
-----
Running a file
^^^^^^^^^^^^^^
If you plan to just run the normal source code (recommended), just pass neutron as the package and the normal arguments after. Make sure you are in the main directory, and not in the `neutron-repo/neutron` path. Example:

.. code-block:: bash

 pypy neutron path/to/neutron/file.ntn  # Faster than python3

 # OR

 python3 neutron path/to/neutron/file.ntn  # Using default python implementation (slower)

To use neutron, pass the filename as the first argument to the neutron binary if you built it from source.

.. code-block:: bash

 python3 ./neutron path/to/neutron/file.ntn

Optional Flags
^^^^^^^^^^^^^^
Verbose
*******
Option: ``--verbose`` or ``-v``

Info: make neutron print out the parse tree and the tokens and general debug info.

Example: ``neutron file.ntn -v``

Writing Neutron
---------------
.. toctree::
  :maxdepth: 1
  :caption: Syntax:

  core_syntax/comments
  core_syntax/primitive_types
  core_syntax/collection_types
  core_syntax/operators
  core_syntax/variables
  core_syntax/conditionals
  core_syntax/functions
  core_syntax/classes
  core_syntax/loops
  core_syntax/delete
  core_syntax/builtin_functions
