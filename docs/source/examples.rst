Examples
========

Guess The Number Game
---------------------
.. code-block:: java

  get!("io/print");
  get!("io/stdin");
  get!("types/to_int");
  get!("types/to_string");
  get!("random/randrange");


  is_not_win = true;
  number = randrange(0, 100);
  num_guesses = 0;

  while (is_not_win) {
    guess = to_int(stdin(prompt="Enter A Number Between 0 and 100: "));
    if (guess == number) {
      print("You Win!");
      is_not_win = false;
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
