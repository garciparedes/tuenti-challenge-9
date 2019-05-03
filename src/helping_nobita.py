import re
import itertools as it
from collections import Counter
from typing import Tuple, List

KANJI_CHAR_TO_INT = {
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9,
    '十': 10,
    '百': 100,
    '千': 1000,
    '万': 10000,
}

KANJI_INT_TO_CHAR = {v: k for k, v in KANJI_CHAR_TO_INT.items()}

QUANTIFIERS = [10, 100, 1000, 10000]


class EquationException(Exception):
    pass


def process_message(message: str) -> Tuple[str, str, str]:
    matched = re.match(r'(?P<a>.+) OPERATOR (?P<b>.+) = (?P<c>.+)', message)
    a, b, c = matched.group('a', 'b', 'c')
    return a, b, c


def build_generator(digits: List[int], kanji: str):
    mapping = it.permutations(digits)
    mapping = map(lambda x: int(''.join(map(str, x))), mapping)
    kanji_counter = Counter(kanji)
    mapping = filter(lambda x: Counter(compose_kanji(x)) == kanji_counter, mapping)
    return mapping


def compose_kanji(number: int) -> str:
    kanji = str()
    for base, digit in enumerate(reversed(str(number))):
        digit = int(digit)
        quantifier = 10 ** base
        if digit == 0:
            continue
        if quantifier > 1:
            kanji += KANJI_INT_TO_CHAR[quantifier]
        if quantifier == 1 or digit != 1 or quantifier == 10000:
            kanji += KANJI_INT_TO_CHAR[digit]
    kanji = ''.join(reversed(kanji))
    return kanji


def from_kanji(kanji: str):
    numbers = list(map(lambda c: KANJI_CHAR_TO_INT[c], kanji))

    quantifiers = list(filter(lambda x: x in QUANTIFIERS, numbers))
    digits = filter(lambda x: x not in QUANTIFIERS, numbers)

    digits = list(digits)
    if quantifiers:
        n_digits = len(str(max(*quantifiers, 1)))
        while len(digits) < n_digits:
            digits.append(0)

    yield from build_generator(digits, kanji)

    for _ in quantifiers:
        if 0 not in digits:
            break
        digits.remove(0)
        digits.append(1)
        yield from build_generator(digits, kanji)


def obtain_op(a: int, b: int, c: int) -> chr:
    if a + b == c:
        return '+'
    elif a - b == c:
        return '-'
    elif a * b == c:
        return '*'
    else:
        raise EquationException


def solve_case() -> str:
    message = input().strip()

    a_kanji, b_kanji, c_kanji = process_message(message)

    a_digits = from_kanji(a_kanji)
    b_digits = from_kanji(b_kanji)
    c_digits = from_kanji(c_kanji)

    for a, b, c in it.product(a_digits, b_digits, c_digits):
        try:
            op = obtain_op(a, b, c)
            return f'{a} {op} {b} = {c}'
        except EquationException:
            pass
    raise Exception


def main() -> None:
    n = int(input())

    mapping = map(lambda idx: (idx + 1, solve_case()), range(n))
    for i, solution in mapping:
        print(f'Case #{i}: {solution}')


if __name__ == '__main__':
    main()
