from collections import namedtuple
from copy import deepcopy
from functools import reduce
from math import pi, cos, sqrt
from typing import Iterable, List, Set, Tuple
from dataclasses import dataclass


@dataclass
class Point(object):
    radio: float
    angle: float

    def distance(self, other: 'Point') -> float:
        value = 0.0
        value += self.radio ** 2
        value += other.radio ** 2
        value -= 2 * self.radio * other.radio * cos(self.angle - other.angle)
        distance = sqrt(value)
        return distance


@dataclass
class Moon(object):
    distance: float
    start_radian: float
    period: float
    capacity: int

    @staticmethod
    def list_from_input() -> List['Moon']:
        m = int(input())
        distances = tuple(map(float, input().split()))
        radians = tuple(map(float, input().split()))
        periods = tuple(map(float, input().split()))
        capacities = tuple(map(int, input().split()))
        moons = list(Moon(*args) for args in zip(distances, radians, periods, capacities))
        return moons

    def position(self, time: float) -> Point:
        standardized_time = time % self.period
        delta_radians = (standardized_time * 2 * pi / self.period)
        radians = (self.start_radian + delta_radians) % (2 * pi)
        return Point(self.distance, radians)

    def distance_to(self, other: 'Moon' = None, time: float = None):
        if other is None:
            return self.distance

        p1 = self.position(time)
        p2 = other.position(time)
        distance = p1.distance(p2)
        return distance


@dataclass
class Ship(object):
    capacity: int
    ship_range: float
    load: int = 0

    @staticmethod
    def from_input() -> 'Ship':
        c = int(input())
        r = float(input())
        return Ship(c, r)


def explore(ship: Ship, moons: List[Moon], path=None, time: float = 0.0,
            loads=None, distance: float = 0.0) -> List[int]:
    if loads is None:
        loads = list()

    if path is None:
        path = list()
        current = None
    else:
        current = path[-1]

    visited = list()
    for moon in moons:
        going_distance = moon.distance_to(current, time)
        return_distance = moon.distance_to(None, time)

        if not (sum(loads) + moon.capacity <= ship.capacity):
            visited = list(loads) if sum(loads) > sum(visited) else visited
            continue

        if not (distance + going_distance + return_distance <= ship.ship_range):
            visited = list(loads) if sum(loads) > sum(visited) else visited
            continue

        current_moons = list(moons)
        current_moons.remove(moon)

        current_path = path + [moon]
        current_loads = loads + [moon.capacity]
        if not current_moons:
            visited = list(current_loads) if sum(current_loads) > sum(visited) else visited
            continue

        current_visited = explore(ship, current_moons, current_path, time + 6, current_loads, distance + going_distance)

        visited = list(current_visited) if sum(current_visited) > sum(visited) else visited

    return visited


def solve_case() -> List[int]:
    moons = Moon.list_from_input()
    ship = Ship.from_input()

    visited = explore(ship, moons)
    visited.sort()
    return visited


def unpack(s: Iterable) -> str:
    return " ".join(map(str, s))


def main():
    n = int(input())
    mapping = map(lambda idx: (idx + 1, solve_case()), range(n))
    for i, solution in mapping:
        print(f'Case #{i}: {unpack(solution) if solution else "None"}')


if __name__ == '__main__':
    main()
