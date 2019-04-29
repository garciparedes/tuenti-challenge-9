from math import ceil


def solve(i: int) -> str:
    n, m = map(float, input().split())
    count = ceil(n / 2) + ceil(m / 2)
    return f'Case #{i}: {count}'


def main():
    c = int(input().strip())
    mapping = map(solve, range(1, c + 1))
    for result in mapping:
        print(result)


if __name__ == '__main__':
    main()
