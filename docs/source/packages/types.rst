Type Package
^^^^^^^^^^^^
This package is responsible for the conversion of types.

``types/to_int``
================
``to_int(obj)`` converts any given object to ``IntType``. (``FloatType``, ``StringType``, etc.)

``types/to_string``
===================
``to_string(obj)`` converts any given object to ``StringType``. (``FloatType``, ``BoolType``, etc.)

``types/to_float``
==================
``to_float(obj)`` converts any given object to ``FloatType``. (``IntType``, ``StringType``, etc.)

``types/to_numpy``
==================
``to_numpy(obj)`` converts any given object to ``NumpyArray``. (``ListType``, ``TupleType``, etc.)

``types/to_list``
=================
``to_list(obj)`` converts any given object to ``ListType``. (``NumpyArray``, ``TupleType``, etc.)

``types/to_tuple``
==================
``to_tuple(obj)`` converts any given object to ``TupleType``. (``ListType``, ``NumpyArray``, etc.)
