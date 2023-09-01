def convertToFahrenheit(degreesCelsius: int) -> float:
    """Converts the temperature from celsius to fahreinheit.

    Args:
        degreesCelsius (int): An integer representing the temperature in Celsius.

    Returns:
        float: An integer representing the temperature converted to Fahreinheight.
    """
    try:
        return degreesCelsius * (9 / 5) + 32
    except TypeError:
        return print("Not a number. Try again")  # type: ignore


def convertToCelsius(degreesFahrenheit: int) -> float:
    """Converts the temperature from fahreinheit to celcius.

    Args:
        degreesFahrenheit (int): An integer representing the temperature in Fahreinheit.

    Returns:
        float: An integer representing the temperature converted to Celcius.
    """
    try:
        return (degreesFahrenheit - 32) * (5 / 9)
    except TypeError:
        return print("Not a number. Try again")  # type: ignore


assert convertToCelsius(0) == -17.77777777777778
assert convertToCelsius(180) == 82.22222222222223
assert convertToFahrenheit(0) == 32
assert convertToFahrenheit(100) == 212
assert convertToCelsius(convertToFahrenheit(15)) == 15  # type: ignore
