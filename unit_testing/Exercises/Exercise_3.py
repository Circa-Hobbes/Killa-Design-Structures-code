def fizzBuzz(upTo: int):
    """Fizz buzz exercise. The usual.

    Args:
        upTo (int): An integer that we loop through
    """
    output = []
    for i in range(1, upTo + 1):
        if i % 3 == 0 and i % 5 == 0:
            output.append("FizzBuzz")
        elif i % 3 == 0:
            output.append("Fizz")
        elif i % 5 == 0:
            output.append("Buzz")
        else:
            output.append(str(i))
    return print(" ".join(output))


fizzBuzz(35)
