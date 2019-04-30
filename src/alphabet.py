from collections import defaultdict
from itertools import chain
from typing import Set, Dict, List


class AlphabetException(Exception):
    pass


def build_graph(words, max_len):
    graph = defaultdict(set)
    for i in range(max_len):
        for w1, w2 in zip(words[:-1], words[1:]):
            if len(w1) <= i:
                continue
            if len(w2) <= i:
                continue
            if w1[:i] != w2[:i]:
                continue
            if w1[i] == w2[i]:
                continue
            graph[w1[i]].add(w2[i])
    return graph


def deep_first_search(graph: Dict[str, Set[str]], node, seen: List[str] = None,
                      path: List[str] = None) -> List[List[str]]:
    if seen is None:
        seen = list()
    if path is None:
        path = [node]

    seen.append(node)

    paths = list()
    for t in graph[node]:
        if t not in seen:
            t_path = path + [t]
            paths.append(tuple(t_path))
            paths.extend(deep_first_search(graph, t, seen[:], t_path))
    return paths


def generate_ordered(graph, head, chars):
    if len(graph) < 1:
        return [head]

    all_paths = deep_first_search(graph, head)
    max_len = max(len(p) for p in all_paths)
    max_paths = [p for p in all_paths if len(p) == max_len]

    if len(max_paths) != 1:
        raise AlphabetException
    ordered = max_paths[0]

    if len(ordered) != len(chars):
        raise AlphabetException

    return ordered


def get_head(graph, chars) -> chr:
    heads = chars.difference(chain(*graph.values()))
    if len(heads) != 1:
        raise AlphabetException
    head = heads.pop()
    return head


def solve_case() -> str:
    m = int(input())

    words = list()
    max_word_len = 0
    chars = set()
    for _ in range(m):
        word = input()
        words.append(word)
        max_word_len = max(max_word_len, len(word))
        chars.update(*word)

    graph = build_graph(words, max_word_len)
    try:
        head = get_head(graph, chars)
        ordered = generate_ordered(graph, head, chars)
    except AlphabetException:
        return 'AMBIGUOUS'
    return ' '.join(ordered)


def main():
    n = int(input())

    mapping = map(lambda idx: (idx + 1, solve_case()), range(n))
    for i, result in mapping:
        print(f'Case #{i}: {result}')


if __name__ == '__main__':
    main()
