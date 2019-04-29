from typing import Tuple

MATRIX = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '-'],
]


def find(c: chr) -> Tuple[int, int]:
    for i, row in enumerate(MATRIX):
        try:
            j = row.index(c)
            return i, j
        except ValueError:
            pass


def decrypt(x, y, message) -> str:
    result = str()
    for c in message:
        if c != ' ':
            a, b = find(c)
            result += MATRIX[(a + x) % len(MATRIX)][(b + y) % len(MATRIX[0])]
        else:
            result += ' '
    return result


def solve_case() -> str:
    who = input().strip()
    message = input().strip()

    a, b = find(who)
    x, y = find(message[-1])

    x_offset = a - x
    y_offset = b - y

    return decrypt(x_offset, y_offset, message)


def main():
    n = int(input())
    mapping = map(lambda i: (solve_case(), i + 1), range(n))
    for result, i in mapping:
        print(f'Case #{i}: {result}')


if __name__ == '__main__':
    main()
