.. neutron documentation master file, created by
   sphinx-quickstart on Sun May 26 20:16:13 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Neutron: A Programming Language
===============================

This is the official documentation for `neutron-lang <https://github.com/MonliH/neutron>`_.
Neutron is a dynamically typed programming language implemented in `Python 3 <https://www.python.org/>`_.
It is inspired by C, Java, and Python. Neutron uses a LALR\(1\) parser to parse its grammar, and the `SLY <https://github.com/dabeaz/sly>`_ parsing library.
Neutron is an interpreted language (for now...).

Design Principles
^^^^^^^^^^^^^^^^^

- **Be easy to read.** Neutron has been designed to be easy to read, and easy to learn.
  It is similar to Python 3, making it easier to learn for those who know the language. It also does not use newlines (`Off-side Rule <https://en.wikipedia.org/wiki/Off-side_rule>`_)
  which makes it easier to learn for people coming from languages like C and C++.

- **Have a consistent syntax.** Neutron's syntax was designed to be elegant and consistent. It does **not** have many exceptions/inconsistencies as far as syntax is concerned.

- **Be different.** You might be thinking, why would I ever use this over Python?
  It's just another language to learn, and it provides the same features as a lot of other programming languages.
  That's where your wrong. Neutron is going to have **C-like structs, switch statements, and more**. Oh, and also it has **built-in Numpy support** and **built-in functions**.

.. toctree::
   :maxdepth: 3
   :caption: Documentation Contents:

   features
   examples
   introduction
   customization
   license
   faq



Indices and tables
^^^^^^^^^^^^^^^^^^

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
