import time
from typing import List, Optional, Tuple

import cv2
import numpy as np


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def __mul__(self, other: int) -> 'Point':
        return Point(self.x * other, self.y * other)

    def __floordiv__(self, other: int) -> 'Point':
        return Point(self.x // other, self.y // other)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'


class Map:
    def __init__(self, map: List[str], scale: int) -> None:
        self.__map = map
        self.__scale = scale
        column_count = len(map[0])
        for row in map:
            assert len(row) == column_count, 'All rows must have the same length.'

    @property
    def scale(self) -> int:
        return self.__scale

    @property
    def width(self) -> int:
        return len(self.__map[0]) * self.scale

    @property
    def height(self) -> int:
        return len(self.__map) * self.scale

    def is_grass(self, cell: Point) -> bool:
        return self.__map[cell.y // self.scale][cell.x // self.scale] == '1'

    def is_sand(self, cell: Point) -> bool:
        return self.__map[cell.y // self.scale][cell.x // self.scale] == '2'

    def is_water(self, cell: Point) -> bool:
        return self.__map[cell.y // self.scale][cell.x // self.scale] == '3'

    def is_floor(self, cell: Point) -> bool:
        return self.is_grass(cell) or self.is_sand(cell) or self.is_water(cell)

    def is_wall(self, cell: Point) -> bool:
        return self.__map[cell.y // self.scale][cell.x // self.scale] == '#'

    def cost(self, previous: Point, new: Point) -> int:
        cost = 0
        if self.is_grass(previous):
            cost += 1
        elif self.is_sand(previous):
            cost += 3
        else:
            cost += 9
        if self.is_grass(new):
            cost += 1
        elif self.is_sand(new):
            cost += 3
        else:
            cost += 9
        return cost // 2

    def draw(self) -> np.ndarray:
        image = np.zeros((self.height // self.scale * 5, self.width // self.scale * 5, 3), dtype=np.uint8)
        for y in range(self.height // self.scale):
            for x in range(self.width // self.scale):
                if self.is_wall(Point(x * self.scale, y * self.scale)):
                    image[y * 5:(y + 1) * 5, x * 5:(x + 1) * 5] = [0, 0, 0]
                elif self.is_grass(Point(x * self.scale, y * self.scale)):
                    image[y * 5:(y + 1) * 5, x * 5:(x + 1) * 5] = [0, 255, 0]
                elif self.is_sand(Point(x * self.scale, y * self.scale)):
                    image[y * 5:(y + 1) * 5, x * 5:(x + 1) * 5] = [0, 165, 255]
                else:
                    image[y * 5:(y + 1) * 5, x * 5:(x + 1) * 5] = [255, 255, 0]
        return image


def find_path_to_castle(map: Map, start: Point, castle: Point) -> Optional[List[Point]]:
    """
    Finds the closest tree to the given point on the map.

    Params:
    -------
    map: Map
        Map object containing the map data.
    start: Point
        Starting point to search for the closest tree.
    castle: Point
        Ending point to reach.

    Returns:
    --------
    List[Point]
        List of points on the path to the closest tree.
        If no tree is found, returns None.
    """
    pass


def draw_path(map: Map, path: List[Point], start_time: float) -> None:
    """
    Draws the path on the map.

    Params:
    -------
    map: Map
        Map object containing the map data.
    path: List[Point]
        List of points on the path to draw.
    """
    image = map.draw()
    player = path[0] // map.scale
    image[player.y * 5:(player.y + 1) * 5, player.x * 5:(player.x + 1) * 5] = [255, 0, 0]
    castle = path[-1] // map.scale
    image[castle.y * 5:(castle.y + 1) * 5, castle.x * 5:(castle.x + 1) * 5] = [100, 100, 100]
    for i in range(len(path) - 1):
        previous_point = path[i] // map.scale
        next_point = path[i + 1] // map.scale
        if previous_point == next_point:
            continue
        cv2.line(
            image,
            (previous_point.x * 5 + 2, previous_point.y * 5 + 2),
            (next_point.x * 5 + 2, next_point.y * 5 + 2),
            (0, 0, 255),
            2)
    cv2.imshow('Path', image)
    cv2.waitKey(max(100, int((1 - (time.time() - start_time)) * 1000)))


if __name__ == '__main__':
    map_version = 1

    if map_version == 1:
        map_array = [
            '#########',
            '#1121111#',
            '#1111213#',
            '#1211111#',
            '#########'
        ]
        scale = 1
        map = Map(map_array, scale)
        castle = Point(6, 2) * scale
    elif map_version == 2:
        map_array = [
            '#########',
            '#2111111#',
            '#2#####3#',
            '#1111113#',
            '#########'
        ]
        scale = 1
        map = Map(map_array, scale)
        castle = Point(7, 1) * scale
    else:
        map_array = [
            '#########',
            '#1112331#',
            '#1112111#',
            '#1111331#',
            '#########'
        ]
        scale = 50
        map = Map(map_array, scale)
        castle = Point(7 * scale + scale // 2, 3 * scale + scale // 2)

    for y in range(map.height // scale):
        for x in range(map.width // scale):
            start = Point(x * scale + scale // 2, y * scale + scale // 2)
            if map.is_floor(start) and start != castle:
                start_time = time.time()
                castle_path = find_path_to_castle(map, start, castle)
                if castle_path:
                    draw_path(map, castle_path, start_time)

    cv2.destroyAllWindows()
