from functools import partial
from itertools import chain
from typing import Tuple, Iterable

Coordinate = Tuple[int, int]

UNFOLD = {
    'L': lambda c, w, h: ((w - c[0] - 1, c[1]), (w + c[0], c[1])),
    'R': lambda c, w, h: ((c[0], c[1]), (2 * w - c[0] - 1, c[1])),
    'T': lambda c, w, h: ((c[0], h - c[1] - 1), (c[0], h + c[1])),
    'B': lambda c, w, h: ((c[0], c[1]), (c[0], 2 * h - c[1] - 1)),
}


def unfold(fold: chr, punches: Iterable[Coordinate], w: int, h: int):
    fn = partial(UNFOLD[fold], w=w, h=h)
    mapping = map(fn, punches)
    mapping = chain(*mapping)
    return mapping


def update_dimensions(w: int, h: int, fold: chr) -> Tuple[int, int]:
    if fold in ('L', 'R'):
        w *= 2
    else:
        h *= 2
    return w, h


def solve_case() -> str:
    w, h, f, p = map(int, input().split())

    folds = list()
    for _ in range(f):
        folds.append(input().strip())

    punches = list()
    for _ in range(p):
        punch = tuple(map(int, input().split()))
        punches.append(punch)

    for fold in folds:
        punches = unfold(fold, punches, w, h)
        w, h = update_dimensions(w, h, fold)
    punches = sorted(punches)

    return '\n'.join(map(lambda c: ' '.join(map(str, c)), punches))


def main():
    n = int(input())
    mapping = map(lambda i: (solve_case(), i + 1), range(n))
    for result, i in mapping:
        print(f'Case #{i}:\n{result}')


if __name__ == '__main__':
    main()
