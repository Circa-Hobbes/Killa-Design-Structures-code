from functools import cache
import timeit


@cache
def test(x, y):
    return x * y


print(test(10, 10))
