Loops
=====
While Loops
-----------
While loops are like while loops in python. They keep on looping until a certain condition is false. This condition is put in parentheses and the code that is to be run is but in curly braces. Example:

.. code-block:: neutron

  x = 0;  // Declare variable x
  while (x < 10) {  // Check if x is greater than 10, if so, break out of loop
    x += 1;
  }
  // now x == 10

For Loops
---------
For loops are just like for loops in python. They iterate through an object, and repeat until the object "over". Neutron uses the ``in`` keyword for its iteration. Example:

.. code-block:: neutron

  list_thing = [1, 2, 3, 4, 5, 6, 7, 8];
  for i in list_thing {
    // do something with i
  }

Break Statements
----------------
To break out of a loop, simply use the ``break`` keyword. Example:

.. code-block:: neutron

  while (true) {
    break;
  }

  for i in foo {
    break;
  }

Make sure not to break inside a program or an area that is not a loop. Doing so may result in glitches and errors. Note that if you have nested while loops, ``break`` will break out of the one that it is put in.
A break statement can also be used in a function, and if called in a loop, will break out of it. Example:

.. code-block:: neutron

  func break_func() {
    break;
  }

  while (true) {
    break_func(); // Breaks out of loop
  }
