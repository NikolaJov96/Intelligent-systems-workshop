from abc import ABC, abstractmethod
from math import pi, sin


class FrequencySpectrum(ABC):
    """
    Base class for frequency spectrum.
    """
    def __init__(self, left_edge: int, right_edge: int):
        self.__left_edge = left_edge
        self.__right_edge = right_edge

    @abstractmethod
    def check_clarity(self, frequency: int) -> float:
        pass

    @property
    def left_edge(self) -> int:
        return self.__left_edge

    @property
    def right_edge(self) -> int:
        return self.__right_edge


class TriangleSpectrum(FrequencySpectrum):
    """
    Spectrum resembling a triangle, describing one radio station.
    """
    def __init__(self):
        super().__init__(50, 150)

    def check_clarity(self, frequency: int) -> float:
        if frequency < self.left_edge or frequency > self.right_edge:
            return 0

        if frequency < 100:
            return frequency
        else:
            return 200 - frequency


class DoubleSinSpectrum(FrequencySpectrum):
    """
    Spectrum consisting of 2 sin periods, describing two radio stations.
    """
    def __init__(self):
        super().__init__(50, 150)

    def check_clarity(self, frequency: int) -> float:
        if frequency < self.left_edge or frequency > self.right_edge:
            return 0

        # Stretch 2 sin periods in the range [50, 150]
        return 25 * sin(2 * (frequency - 112.5) * 2 * pi / 100) + 75


class TripleSinSpectrum(FrequencySpectrum):
    """
    Spectrum consisting of 3 sin periods, describing 3 radio stations.
    """
    def __init__(self):
        super().__init__(1000, 1600)

    def check_clarity(self, frequency: int) -> float:
        if frequency < self.left_edge or frequency > self.right_edge:
            return 0

        # Stretch 3 sin periods in the range [1000, 1600]
        return 25 * sin(3 * (frequency - 1050) * 2 * pi / 600) + 75
