Classes
=======
Classes in Neutron are very similar to those in python. Right now, there are magic methods, like python. Here is a list of python-like magic methods:

- ``--init--`` - is run when an instance of the class is made

They are an object, and any function defined in the class will be defined. Classes are used through methods, which are really just functions defined in a class.

Defining a Class
----------------
To make a class, use the ``class`` keyword, and provide the name of the class after. Inside the class, define functions that you want to make into methods. Note that instead of ``self``, like in python, the ``this`` argument should be used, in fact, if you don't use the the ``this`` argument as your first argument, the neutron interpreter will complain. Example:

.. code-block:: neutron

  class MyClass {
    func --init--(this, foo) {
      this::foo = 10;
      this::numpy_array = (230, 34, 23);
    }
    func return_numpy_array(this) {
      --return-- = this::numpy_array;
    }
  }

Note that you can also use the special variable ``--return--`` in a method.

Making Instance of Class
------------------------
To make an instance of a class, simply just call the class like a function, and provide the arguments needed by the ``--init--`` method. Note that the ``this`` argument is passed by the neutron interpreter. For example:

.. code-block:: neutron

  class MyClass {
    func --init--(this, _foo) {  // Don't pollute variables
      this::foo = _foo;
      this::numpy_array = (230, 34, 23);
    }
    func return_numpy_array(this) {
      --return-- = this::numpy_array;
    }
  }

  instance_of_my_class = MyClass(123);  // Make instance of MyClass

Now, ``instance_of_my_class`` is an instance of the ``MyClass`` class.

Running Methods
---------------
To run a method, simply use double colons and a pair of parentheses. Note that you also don't need to provide the ``this`` argument either, because the neutron interpreter does it for you. Example:

.. code-block:: neutron

  instance_of_my_class = MyClass(123);  // Make instance of MyClass
  my_array = instance_of_my_class::return_numpy_array();  // Run return_numpy_array method on MyClass

Getting and Setting Attributes
------------------------------
To set and get attributes, simply just assign values using a single equals sign. Example:

.. code-block:: neutron

  instance_of_my_class::array = [12, 45, 23, 42, 87];  // Redefine array attribute in instance_of_my_class
  x = instance_of_my_class::foo;  // Assign x to the value of instance_of_my_class's attribute foo
