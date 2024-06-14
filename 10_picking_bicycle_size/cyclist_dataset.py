import random
from enum import Enum
from typing import List, Optional, Tuple

from matplotlib import pyplot as plt


class BicycleSize(Enum):
    XS = 0
    S = 1
    M = 2
    L = 3
    XL = 4


class Cyclist:
    def __init__(self, height: float, leg_length: float, arm_length: float):
        self.__height = height
        self.__leg_length = leg_length
        self.__arm_length = arm_length

    @property
    def height(self) -> float:
        return self.__height

    @property
    def leg_length(self) -> float:
        return self.__leg_length

    @property
    def arm_length(self) -> float:
        return self.__arm_length

    def __repr__(self) -> str:
        return f'Cyclist(height={self.height}, leg_length={self.leg_length}, arm_length={self.arm_length})'


def create_bicycle_dataset(
        dataset_size: int,
        deviation_scale: float = 1.0,
        random_seed: int = 37) -> List[Tuple[Cyclist, BicycleSize]]:
    """
    Creates a dataset of cyclists with their respective bicycle sizes.

    Parameters
    ----------
    size : int
        The size of the dataset.
    random_seed : int
        The random seed for reproducibility.

    Returns
    -------
    List[Tuple[Cyclist, BicycleSize]]
        The dataset of cyclists with their respective bicycle sizes.
    """
    random.seed(random_seed)

    start_height = 150
    end_height = 200

    dataset = []
    for i in range(dataset_size):
        base_height = start_height + (end_height - start_height) * i / dataset_size
        bike_size = BicycleSize(i * len(BicycleSize) // dataset_size)

        height = random.normalvariate(base_height, 3.5 * deviation_scale)
        leg_length = random.normalvariate(0.5 * height, 2 * deviation_scale)
        arm_length = random.normalvariate(0.4 * height, 2 * deviation_scale)

        cyclist = Cyclist(height, leg_length, arm_length)
        dataset.append((cyclist, bike_size))

    return dataset


def plot_bicycle_dataset(dataset: List[Tuple[Cyclist, BicycleSize]], title: str, cyclist: Optional[Cyclist] = None) -> None:
    """
    Plots the dataset of cyclists with their respective bicycle sizes.

    Parameters
    ----------
    dataset : List[Tuple[Cyclist, BicycleSize]]
        The dataset of cyclists with their respective bicycle sizes.
    cyclist : Optional[Cyclist]
        The cyclist to highlight in the plot.
    """
    size_colors = plt.cm.nipy_spectral([i / len(BicycleSize) for i in range(len(BicycleSize))])

    xs = [cyclist.arm_length for cyclist, _ in dataset]
    ys = [cyclist.leg_length for cyclist, _ in dataset]
    zs = [cyclist.height for cyclist, _ in dataset]
    colors = [size_colors[size.value] for _, size in dataset]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xs, ys, zs, c=colors)

    if cyclist is not None:
        ax.scatter(cyclist.arm_length, cyclist.leg_length, cyclist.height, c='red', s=100)

    ax.set_xlabel('Arm Length')
    ax.set_ylabel('Leg Length')
    ax.set_zlabel('Height')
    ax.set_title(title)
    ax.legend(handles=[
        plt.Line2D([0], [0], marker='o', color='w', label=size.name, markerfacecolor=color, markersize=10)
        for size, color in zip(BicycleSize, size_colors)
    ])

    plt.show()
