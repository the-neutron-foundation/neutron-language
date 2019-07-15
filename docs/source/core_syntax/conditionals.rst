Conditionals
============
Conditionals work around the same in python.

If
----
If statements use the ``if`` keyword, followed by the condition in parentheses, followed by the code to run. Example:

.. code-block:: neutron

  if (true) {
    // run code here
  }

Else If
-------
Else if statements use the ``else`` and ``if`` keyword, followed by the condition in parentheses, followed by the code to run. They go after if statements and are run if the previous if statement evaluated to ``false``. Note the python ``elif`` keyowrd does not work. Example:

.. code-block:: neutron

  if (false) {
    // code that won't run
  } else if (true) {
    // run code here
  }

Else
----
Else if statements also go after if or else if statements, and are run when everything before it evaluated to false. They do not need a condition and use the ``else`` keyword. Example:

.. code-block:: neutron

  if (false) {
    // code that won't run
  } else if (false) {
    // code that won't run
  } else {
    // code that will run
  }
