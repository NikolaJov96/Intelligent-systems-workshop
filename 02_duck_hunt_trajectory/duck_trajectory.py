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


def is_trajectory_valid(
        screen_width: int,
        screen_height: int,
        grass_height: int,
        trajectory: ZigZagTrajectory) -> bool:
    """
    Check if the trajectory is valid, as explained in the `generate_trajectory` function.
    """
    points = trajectory.to_points()
    if points[0].x < 0 or points[0].x >= screen_width or \
            points[0].y < screen_height - grass_height or points[0].y >= screen_height:
        return False
    for point in points[1:-1]:
        if point.x < 0 or point.x >= screen_width or point.y < 0 or point.y >= screen_height - grass_height:
            return False
    if points[-1].y >= screen_height - grass_height:
        return False
    if points[-1].x >= 0 and points[-1].x < screen_width and points[-1].y >= 0 and points[-1].y < screen_height:
        return False
    return True


def generate_trajectory(
        screen_width: int,
        screen_height: int,
        grass_height: int,
        directions_count: int) -> ZigZagTrajectory:
    """
    Generate a trajectory of the duck.

    The trajectory starts under the grass. The duck files in a zigzag pattern. The zigzag
    pattern has a total of `directions_count` directions. For each straight, this function
    returns the angle of the new direction and the distance to the next point. The duck
    should not leave the screen or go under the grass. The final point of the trajectory
    should be outside the screen.

    The [0, 0] point is the top-left corner of the screen.
    The angle 0 is to the right, 90 is down, 180 is left, and 270 is up.

    Args:
        screen_width: The width of the screen.
        screen_height: The height of the screen.
        grass_height: The height of the grass.
        directions_count: The number of directions in the trajectory.

    Returns:
        The trajectory of the duck.
    """
    min_straight_length = screen_width // 10
    max_straight_length = screen_width // 2
    start = Point(screen_width // 2, screen_height - grass_height + 1)
    trajectory = ZigZagTrajectory(start, [])
    while not is_trajectory_valid(screen_width, screen_height, grass_height, trajectory):
        straights = []
        for _ in range(directions_count):
            angle = np.random.uniform(0, 360)
            length = np.random.uniform(min_straight_length, max_straight_length)
            straights.append((angle, length))
        trajectory = ZigZagTrajectory(start, straights)
    return trajectory


if __name__ == '__main__':
    screen_width = 800
    screen_height = 600
    grass_height = 100
    directions_count = 10

    while True:
        trajectory = generate_trajectory(screen_width, screen_height, grass_height, directions_count)

        image = np.zeros((screen_height, screen_width, 3), np.uint8)
        image[screen_height - grass_height:, :] = [0, 255, 0]
        image[:screen_height - grass_height, :] = [255, 155, 0]
        trajectory.draw(image)

        cv2.imshow('Duck trajectory', image)
        key = cv2.waitKey(0)
        if key == 27:
            break
    cv2.destroyAllWindows()
