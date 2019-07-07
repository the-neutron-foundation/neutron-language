File Package
^^^^^^^^^^^^
The ``file`` package deals with the reading and writing of files.

``file/file``
=============
``file(filename)`` is a file object with the methods: ``read``, ``write`` and ``append``. The `filename` (string) should (for now) be the absolute path of the file you wish to read/write to.

``file/file::read()``
=====================
``file(filename)::read()`` reads the file given and returns the contents of that file. It takes no arguments

``file/file::write()``
======================
``file(filename)::write(text)`` write to a file and returns nothing (``NullType``). It takes the argument of what to write to that file.

``file/file::append()``
=======================
``file(filename)::append(text)`` append to an existing file and returns nothing (``NullType``). It takes the argument of what to append to that file.
