from typing import List, Tuple

import cv2
import numpy as np


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class ZigZagTrajectory:
    def __init__(self, start: Point, straights: List[Tuple[float, float]]):
        """
        Defines a zigzag trajectory.

        Args:
            start: The starting point of the trajectory.
            straights: A list of tuples with the angle in degrees and length of each straight.
        """
        self.start = start
        self.straights = straights

    def to_points(self) -> List[Point]:
        """
        Convert the trajectory to a list of points where the direction changes.

        Returns:
            A list of points in the trajectory.
        """
        points = [Point(self.start.x, self.start.y)]
        point_x, point_y = self.start.x, self.start.y
        for angle, length in self.straights:
            point_x += length * np.cos(np.radians(angle))
            point_y += length * np.sin(np.radians(angle))
            points.append(Point(point_x, point_y))
        return points

    def draw(self, image: np.ndarray) -> None:
        """
        Draw the trajectory on an image.

        Args:
            image: The image where the trajectory will be drawn.
        """
        point_a_x, point_a_y = int(self.start.x), int(self.start.y)
        for point_b in self.to_points():
            point_b_x, point_b_y = int(point_b.x), int(point_b.y)
            cv2.line(image, (point_a_x, point_a_y), (point_b_x, point_b_y), (255, 255, 255), 2)
            point_a_x, point_a_y = point_b_x, point_b_y
