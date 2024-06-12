import random
from typing import List, Optional

import matplotlib.pyplot as plt


def find_available_computer(available_computers: List[bool]) -> Optional[int]:
    """
    Finds an available computer among the given list of computers.
    Every available computer should have an equal chance of being picked.

    Params:
    -------
    available_computers: List[bool]
        List of boolean values indicating whether a computer is available or not.

    Returns:
    --------
    int
        Index of one of the available computers. If no computer is available, returns None.
    """
    options = list(range(len(available_computers)))
    while len(options) > 0:
        id = random.randint(0, len(options) - 1)
        if available_computers[options[id]]:
            return options[id]
        else:
            options.pop(id)
    return None


if __name__ == '__main__':
    available_computers = [True, False, True, False, True, True, True, False, True, False]
    computer_count = len(available_computers)
    pick_distribution = [0 for _ in range(computer_count)]
    for _ in range(100 * computer_count):
        computer = find_available_computer(available_computers)
        if computer is not None:
            pick_distribution[computer] += 1

    plt.bar(range(computer_count), pick_distribution)
    plt.xticks(range(computer_count), [f'{i}\n{available_computers[i]}' for i in range(computer_count)])
    plt.subplots_adjust(bottom=0.15)
    plt.xlabel('Computer Index')
    plt.ylabel('Picked Count')
    plt.title('Picked Computer Distribution')
    plt.show()
