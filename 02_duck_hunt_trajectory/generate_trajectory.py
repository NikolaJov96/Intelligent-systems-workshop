import cv2
import numpy as np
from trajectory import Point, ZigZagTrajectory


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
    pass


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
