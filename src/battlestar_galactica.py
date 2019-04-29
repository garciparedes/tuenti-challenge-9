from collections import defaultdict


def generate_edges() -> defaultdict:
    p = int(input())
    edges = defaultdict(list)
    for i in range(p):
        raw = input()
        origin, destinations = raw.split(':')
        edges[origin].extend(destinations.split(','))
    return edges


def explore(edges, name):
    paths = 0
    for e in edges[name]:
        if e == 'New Earth':
            paths += 1
        else:
            paths += explore(edges, e)
    return paths


def solve_case() -> int:
    edges = generate_edges()
    paths = explore(edges, 'Galactica')
    return paths


def main():
    c = int(input())
    mapping = map(lambda i: (solve_case(), i), range(1, c + 1))
    for result, i in mapping:
        print(f'Case #{i}: {result}')


if __name__ == '__main__':
    main()
