import math


def quadratic_equation(a: int, b: int, c: int) -> tuple[int, int]:
    d = b**2 - 4 * a * c
    return (-b + (1 + math.isqrt(d - 1))) // a, (-b - (1 + math.isqrt(d - 1))) // a
