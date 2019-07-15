Delete Statement
================
To delete variables, use the ``del`` keyword. Example:

.. code-block:: neutron

  x = 10;
  del x;
  print(x); // returns error (variable_referenced_before_assignment_error)

You can also delete items on a list, for example:

.. code-block:: neutron

  x = [10, 20, 30];
  del x[1];
  print(x); // prints [10, 30]
