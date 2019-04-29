from collections import defaultdict
from fractions import Fraction
from functools import reduce
from typing import Tuple, Dict


def gcd(a, b):
    """
    Compute the greatest common divisor of a and b

    URL: https://gist.github.com/endolith/114336/eff2dc13535f139d0d6a2db68597fad2826b53c3
    """
    while b > 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    """
    Compute the lowest common multiple of a and b

    URL: https://gist.github.com/endolith/114336/eff2dc13535f139d0d6a2db68597fad2826b53c3
    """
    return a * b // gcd(a, b)


def is_valid(counter: Dict[int, int]) -> bool:
    for k, v in counter.items():
        if v % k != 0:
            return False
    return True


def fix_values(counter: Dict[int, int]) -> Dict[int, int]:
    inc = reduce(lcm, counter)
    i = 0
    counter_copy = counter
    while not is_valid(counter_copy):
        counter_copy = counter.copy()
        i += inc
        for k in counter_copy.keys():
            counter_copy[k] *= i
    return counter_copy


def solve_case() -> Tuple[int, int]:
    n = int(input())
    mapping = map(int, input().split())

    counter = defaultdict(int)
    for v in mapping:
        counter[v] += 1

    numerator, denominator = 0, 0
    for k, v in fix_values(counter).items():
        numerator += v
        denominator += v // k
    fraction = Fraction(numerator, denominator)

    return fraction.numerator, fraction.denominator


def main():
    c = int(input())
    mapping = map(lambda i: (solve_case(), i + 1), range(c))
    for result, i in mapping:
        print(f'Case #{i}: {result[0]}/{result[1]}')


if __name__ == '__main__':
    main()
