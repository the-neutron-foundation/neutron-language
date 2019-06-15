Examples
========

Guess The Number Game
---------------------
.. code-block:: java

  // imports
  get!("io/print");
  get!("io/stdin");
  get!("types/to_int");


  is_not_win = true;
  number = 10;  // set number

  while (is_not_win) {
    guess = to_int(stdin(prompt="Enter A Number:"));  // get guess and convert into IntType

    // conditionals
    if (guess == number) {
      print("You Win!");
      is_not_win = false;  // break out of loop
    } else if (guess < number) {
      print("Too Low");
    } else if (guess > number) {
      print("Too High");
    }
  }

Factorial Calculator
--------------------
.. code-block:: java

  get!("io/print");

  x = 10;  // get factorial of 10
  answer = 1;

  while (x > 1) {
    answer = answer * x;
    x = x - 1;
  }

  print(answer);
