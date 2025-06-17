def fizzbuzz(length: int = 15) -> None:
    """
    Plays fizzbuzz, where numbers are counted in order but multiples of 
    three are replaced with "fizz", multiples of five are replaced with
    "buzz" and multiples of both are "fizzbuzz"
    
      
    Parameters: 
    length (int) - Defaults to 10, the number of rounds to play
    """

    result = ""

    for number in range(1, length + 1):
        output = ""
        
        if number % 3 == 0:
            output += "Fizz"

        if number % 5 == 0:
            output += "Buzz"

        if not output: 
            output = str(number)

        result += f"{output}\n"

    print(result[:-1])

def fizzbuzz_modular(length: int = 15, rules: dict = None) -> None:
    """
    Plays fizzbuzz with some arbitrary set of rules

    Parameters:
    length (int) - Number of rounds to play, 10 by default
    rules (dict) - Rules for which to play the game, fizz on 3 and buzz on 5 by default
    """

    if rules is None:
        rules = {
            "Fizz": lambda x: x % 3 == 0,
            "Buzz": lambda x: x % 5 == 0
        }

    result = ""

    for number in range(1, length + 1):
        output = ""

        for word in rules:
            output = output + word if rules[word](number) else output

        if not output:
            output = str(number)

        result += f"{output}\n"

    print(result[:-1])

def fizzbuzz_mod_v2(length: int = 15, rules: dict = {3 : "Fizz", 5 : "Buzz"}) -> None:
    """
    Plays fizzbuzz with some arbitrary set of rules

    Parameters:
    length (int) - Number of rounds to play, 10 by default
    rules (dict) - Rules for which to play the game, fizz on 3 and buzz on 5 by default
    """

    result = ""

    for number in range(1, length + 1):
        output = ""

        for divisor in rules:
            output = output + rules[divisor] if number % divisor == 0 else output

        if not output:
            output = str(number)

        result += f"{output}\n"

    print(result[:-1])

fizzbuzz_mod_v2()