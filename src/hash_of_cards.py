from copy import deepcopy
from functools import reduce
from itertools import starmap
from typing import List, Tuple, Iterable, Set


def read_block() -> str:
    n = int(input())
    text = str()
    for _ in range(n):
        line = input()
        text += line
    text = text.replace('\n', '')
    text = text.replace('\r', '')
    return text


def not_so_complex_hash(text: str, offset: int = 0, base: int = 256) -> List[int]:
    hashed = [0] * 16
    text_bytes = text.encode("iso-8859-1")
    for i in range(len(text_bytes)):
        hashed[(i + offset) % 16] = (hashed[(i + offset) % 16] + text_bytes[i]) % base
    hashed = map(int, hashed)
    return list(hashed)


def sum_two_hashed(hashed_a: List[int], hashed_b: List[int]) -> List[int]:
    mapping = zip(hashed_a, hashed_b)
    mapping = starmap(lambda a, b: (a + b) % 256, mapping)
    return list(mapping)


def sum_hashed(*args) -> List[int]:
    return reduce(sum_two_hashed, args)


def split_block(block: str) -> Tuple[str, str]:
    preamble, body = block.split(''.join(['-'] * 6))
    preamble += '---'
    body = '---' + body
    return preamble, body


def generate_solutions(preamble: str, body: str, hashed: List[int]) -> Tuple[int, List[str]]:
    preamble_hashed = not_so_complex_hash(preamble)

    mapping = (not_so_complex_hash(body, offset=additional + len(preamble)) for additional in range(16))
    mapping = (sum_hashed(v, preamble_hashed) for v in mapping)
    mapping = (list((b - a) % 256 for a, b in zip(v, hashed)) for v in mapping)
    return enumerate(mapping)


def generate_print_section(preamble: str, body: str, hashed: List[int]) -> str:
    offset = len(preamble) % 16

    characters = None
    total_characters = None
    for additional, solution in generate_solutions(preamble, body, hashed):
        new_characters = find_characters(additional, offset, solution)
        new_total_characters = sum(len(v) for v in new_characters)

        if characters is not None and total_characters < new_total_characters:
            continue

        characters = new_characters
        total_characters = new_total_characters

    message = generate_message(characters, offset)

    return message


def generate_message(characters: List[List[int]], offset: int, base: int = 16) -> str:
    message = str()
    i = offset
    while any(len(c) for c in characters):
        message += chr(characters[i].pop(0))
        i = (i + 1) % base
    return message


def available_sizes(possibles: Iterable[List[List[int]]]) -> Set[int]:
    mapping = list(map(lambda x: list(map(len, x)), possibles))
    mapping = list(map(lambda x: set(x), mapping))
    return reduce(set.intersection, mapping)


def generate_result(possibles: List[List[List[int]]], with_one_more) -> List[List[int]]:
    to_check = [v for i, v in enumerate(possibles) if i not in with_one_more]
    sizes = available_sizes(to_check)
    if not sizes:
        return list()
    selected_size = min(sizes)

    to_check = [v for i, v in enumerate(possibles) if i in with_one_more]
    if to_check:
        sizes = available_sizes(to_check)
        if not selected_size + 1 in sizes:
            return list()

    result = list()
    for i, possible in enumerate(possibles):
        w = (i in with_one_more)
        for a in possible:
            if len(a) == selected_size + w:
                result.append(a)
                break
    return result


def update_possibles(solution: List[int], possibles) -> List[int]:
    min_sizes = list(map(lambda x: min(map(len, x)), possibles))
    min_size = min(min_sizes)
    solution = list(x + 256 if min_sizes[i] == min_size else x for i, x in enumerate(solution))
    return solution


def find_characters(additional: int, offset: int, solution: List[int]) -> List[List[int]]:
    with_one_more = set((offset + i) % 16 for i in range(additional))

    solution = list(x if 48 < x else x + 256 for x in solution)
    possibles = list(possible_decomposes(v) for v in solution)
    result = generate_result(possibles, with_one_more)
    while not result:
        solution = update_possibles(solution, possibles)
        possibles = list(possible_decomposes(v) for v in solution)
        result = generate_result(possibles, with_one_more)

    assert solution == list(sum(v) for v in result)
    return result


def possible_decomposes(value: int) -> List[List[int]]:
    if value < 48:
        raise Exception

    result = list()
    if 48 <= value <= 122:
        result += [[value]]

    if 96 <= value <= 170:
        result += [[48, value - 48]]
    if 170 < value <= 244:
        result += [[122, value - 122]]
    if 144 <= value <= 218:
        result += [[48, 48, value - 48 * 2]]
    if 218 < value:
        d1 = possible_decomposes(value - 122)
        d2 = deepcopy(d1)
        for i in range(len(d1)):
            d1[i].append(122)
            d2[i].extend([48, 74])
        result += d1 + d2

    assert all(sum(r) == value for r in result)
    return result


def solve_case():
    original = read_block()
    altered = read_block()

    original_hashed = not_so_complex_hash(original)
    altered_preamble, altered_body = split_block(altered)

    print_section = generate_print_section(altered_preamble, altered_body, original_hashed)

    return print_section


def main():
    n = int(input())
    mapping = map(lambda idx: (idx + 1, solve_case()), range(n))

    for i, result in mapping:
        print(f'Case #{i}: {result}')


if __name__ == '__main__':
    main()
