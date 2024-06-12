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

    def is_grass(self, cell: Point) -> bool:
        return self.__map[cell.y][cell.x] == '1'

    def is_sand(self, cell: Point) -> bool:
        return self.__map[cell.y][cell.x] == '2'

    def is_water(self, cell: Point) -> bool:
        return self.__map[cell.y][cell.x] == '3'

    def is_floor(self, cell: Point) -> bool:
        return self.is_grass(cell) or self.is_sand(cell) or self.is_water(cell)

    def is_tree(self, cell: Point) -> bool:
        return self.__map[cell.y][cell.x] == 'T'

    def is_wall(self, cell: Point) -> bool:
        return self.__map[cell.y][cell.x] == '#'

    def move_cost(self, previous: Point, new: Point) -> int:
        cost = 0
        if self.is_grass(previous):
            cost += 1
        elif self.is_sand(previous):
            cost += 3
        else:
            cost += 9
        if self.is_grass(new) or self.is_tree(previous):
            cost += 1
        elif self.is_sand(new):
            cost += 3
        else:
            cost += 9
        return cost // 2

    def draw(self) -> np.ndarray:
        image = np.zeros((self.height * 5, self.width * 5, 3), dtype=np.uint8)
        for y in range(self.height):
            for x in range(self.width):
                if self.is_wall(Point(x, y)):
                    image[y * 5:(y + 1) * 5, x * 5:(x + 1) * 5] = [0, 0, 0]
                elif self.is_tree(Point(x, y)):
                    image[y * 5:(y + 1) * 5, x * 5:(x + 1) * 5] = [0, 155, 0]
                elif self.is_grass(Point(x, y)):
                    image[y * 5:(y + 1) * 5, x * 5:(x + 1) * 5] = [0, 255, 0]
                elif self.is_sand(Point(x, y)):
                    image[y * 5:(y + 1) * 5, x * 5:(x + 1) * 5] = [0, 165, 255]
                else:
                    image[y * 5:(y + 1) * 5, x * 5:(x + 1) * 5] = [255, 255, 0]
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
    visited_points = {start}
    point_list: List[Tuple[Point, int, List[Point]]] = [(start, 0, [start])]
    while len(point_list) > 0:
        point_list.sort(key=lambda x: x[1])
        current_point, current_cost, current_path = point_list.pop(0)
        if map.is_tree(current_point):
            return current_path
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x = current_point.x + dx
            new_y = current_point.y + dy
            new_point = Point(new_x, new_y)
            if new_point not in visited_points and not map.is_wall(new_point):
                visited_points.add(new_point)
                point_list.append((
                    new_point,
                    current_cost + map.move_cost(current_point, new_point),
                    current_path + [new_point]))
    return None


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
            '#1122333#',
            '#11113T1#',
            '#1111111#',
            '#########'
        ])
    elif map_version == 2:
        map = Map([
            '#########',
            '#211111T#',
            '#2311213#',
            '#T311111#',
            '#########'
        ])
    else:
        map = Map([
            '#########',
            '#111#113#',
            '#2#1#1#3#',
            '#T#111#T#',
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
