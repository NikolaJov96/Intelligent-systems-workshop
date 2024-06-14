from typing import List, Optional, Tuple

import cv2
import numpy as np


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class Map:
    def __init__(self, map: List[str]) -> None:
        self.__map = map
        column_count = len(map[0])
        for row in map:
            assert len(row) == column_count, 'All rows must have the same length.'

    @property
    def width(self) -> int:
        return len(self.__map[0])

    @property
    def height(self) -> int:
        return len(self.__map)

    def is_floor(self, cell: Point) -> bool:
        return self.__map[cell.y][cell.x] == '.'

    def is_wall(self, cell: Point) -> bool:
        return self.__map[cell.y][cell.x] == '#'

    def is_tree(self, cell: Point) -> bool:
        return self.__map[cell.y][cell.x] == 'T'

    def move_cost(self) -> int:
        return 10

    def draw(self) -> np.ndarray:
        image = np.zeros((self.height * 5, self.width * 5, 3), dtype=np.uint8)
        for y in range(self.height):
            for x in range(self.width):
                if self.is_wall(Point(x, y)):
                    image[y * 5:(y + 1) * 5, x * 5:(x + 1) * 5] = [0, 0, 0]
                elif self.is_tree(Point(x, y)):
                    image[y * 5:(y + 1) * 5, x * 5:(x + 1) * 5] = [0, 255, 0]
                else:
                    image[y * 5:(y + 1) * 5, x * 5:(x + 1) * 5] = [255, 255, 255]
        return image


def find_closest_tree(map: Map, start: Point) -> Optional[List[Point]]:
    """
    Finds the closest tree to the given point on the map.

    Params:
    -------
    map: Map
        Map object containing the map data.
    start: Point
        Starting point to search for the closest tree.

    Returns:
    --------
    List[Point]
        List of points on the path to the closest tree.
        If no tree is found, returns None.
    """
    pass


def draw_path(map: Map, path: List[Point]) -> None:
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
    image[path[0].y * 5:(path[0].y + 1) * 5, path[0].x * 5:(path[0].x + 1) * 5] = [255, 0, 0]
    for i in range(len(path) - 1):
        cv2.line(
            image,
            (path[i].x * 5 + 2, path[i].y * 5 + 2),
            (path[i + 1].x * 5 + 2, path[i + 1].y * 5 + 2),
            (0, 0, 255),
            2)
    cv2.imshow('Path', image)
    cv2.waitKey(1000)


if __name__ == '__main__':
    map_version = 1

    if map_version == 1:
        map = Map([
            '#########',
            '#.......#',
            '#.....T.#',
            '#.......#',
            '#########'
        ])
    elif map_version == 2:
        map = Map([
            '#########',
            '#......T#',
            '#.......#',
            '#T......#',
            '#########'
        ])
    else:
        map = Map([
            '#########',
            '#...#...#',
            '#.#.#.#.#',
            '#T#...#T#',
            '#########'
        ])

    for y in range(map.height):
        for x in range(map.width):
            start = Point(x, y)
            if map.is_floor(start):
                tree_path = find_closest_tree(map, start)
                if tree_path:
                    draw_path(map, tree_path)

    cv2.destroyAllWindows()
