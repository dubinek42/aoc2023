import math
from typing import Any

import numpy as np
from numpy.typing import NDArray

neighbors = {
    "left": lambda x: (x[0], x[1] - 1),
    "right": lambda x: (x[0], x[1] + 1),
    "up": lambda x: (x[0] - 1, x[1]),
    "down": lambda x: (x[0] + 1, x[1]),
}


def quadratic_equation(a: int, b: int, c: int) -> tuple[float, float]:
    d = b**2 - 4 * a * c
    return (-b + (1 + math.isqrt(d - 1))) / a, (-b - (1 + math.isqrt(d - 1))) / a


def get_2d_map(s: str) -> NDArray[Any]:
    return np.array([list(x) for x in s.splitlines()])
