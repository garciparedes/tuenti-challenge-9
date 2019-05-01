from functools import reduce
from itertools import starmap, product
from typing import List, Tuple


def read_block() -> str:
    n = int(input())
    text = str()
    for _ in range(n):
        line = input()
        text += line
    text = text.replace('\n', '')
    text = text.replace('\r', '')
    return text


def not_so_complex_hash(text: str, offset: int = 0, base: int = 256) -> Tuple[int]:
    hashed = [0] * 16
    text_bytes = text.encode("iso-8859-1")
    for i in range(len(text_bytes)):
        hashed[(i + offset) % 16] = (hashed[(i + offset) % 16] + text_bytes[i]) % base
    hashed = map(int, hashed)
    return tuple(hashed)


def sum_two_hashed(hashed_a: Tuple[int], hashed_b: Tuple[int]) -> Tuple[int]:
    mapping = zip(hashed_a, hashed_b)
    mapping = starmap(lambda a, b: (a + b) % 256, mapping)
    return tuple(mapping)


def sum_hashed(*args) -> Tuple[int]:
    return reduce(sum_two_hashed, args)


def split_block(block: str) -> Tuple[str, str]:
    preamble, body = block.split(''.join(['-'] * 6))
    preamble += '---'
    body = '---' + body
    return preamble, body


def generate_next_print_section():
    yield ''
    i = 1
    alternatives = list(list(map(chr, range(48, 122 + 1))))
    while True:
        for chars in product(alternatives, repeat=i):
            yield ''.join(chars)
        i += 1


def generate_print_section(hashed: Tuple[int], preamble: str, body: str) -> str:
    generator = generate_next_print_section()
    message = next(generator)

    preamble_hashed = not_so_complex_hash(preamble)
    bodies_hashed = list()
    for i in range(16):
        bodies_hashed.append(not_so_complex_hash(body, offset=i))

    message_hashed = not_so_complex_hash(message, offset=len(preamble))
    body_hashed = bodies_hashed[(len(preamble) + len(message)) % 16]
    modified_hashed = sum_hashed(preamble_hashed, message_hashed, body_hashed)

    while not modified_hashed == hashed:
        message = next(generator)

        message_hashed = not_so_complex_hash(message, offset=len(preamble))

        body_hashed = bodies_hashed[(len(preamble) + len(message)) % 16]
        modified_hashed = sum_hashed(preamble_hashed, message_hashed, body_hashed)

    return message


def solve_case():
    original = read_block()
    altered = read_block()

    original_hashed = not_so_complex_hash(original)
    altered_preamble, altered_body = split_block(altered)

    print_section = generate_print_section(original_hashed, altered_preamble, altered_body)

    return print_section


def main():
    n = int(input())
    mapping = map(lambda idx: (idx + 1, solve_case()), range(n))

    for i, result in mapping:
        print(f'Case #{i}: {result}')


if __name__ == '__main__':
    main()
