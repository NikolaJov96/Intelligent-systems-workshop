from typing import Callable

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from frequency_spectrum import TriangleSpectrum, DoubleSinSpectrum, TripleSinSpectrum


def finetune_radio_station(initial_frequency: int, check_clarity: Callable[[int], float]) -> int:
    """
    Finds the optimal frequency near the initial frequency that provides the best clarity.

    Frequencies are integers and can be searched with the step of 1.
    Any positive integer can be a valid frequency, not just between 88 and 108 MHz.
    Clarity is a float value between 0 and 100.

    Args:
        initial_frequency: The initial frequency set by the user.
        check_clarity: A function that receives a frequency and returns the clarity of the radio station.

    Returns:
        The finetuned frequency.
    """
    best_clarity = check_clarity(initial_frequency)
    best_frequency = initial_frequency
    left_clarity = check_clarity(initial_frequency - 1)
    right_clarity = check_clarity(initial_frequency + 1)
    while best_clarity < max(left_clarity, right_clarity):
        if left_clarity > right_clarity:
            best_frequency -= 1
        else:
            best_frequency += 1
        best_clarity = check_clarity(best_frequency)
        left_clarity = check_clarity(best_frequency - 1)
        right_clarity = check_clarity(best_frequency + 1)
    return best_frequency


def draw_plot(frequencies: np.ndarray, check_clarity: Callable[[int], float]) -> None:
    """
    Draws an animated plot of the radio station clarity for each frequency.

    Args:
        frequencies: An array of frequencies to check the clarity.
        check_clarity: A function that receives a frequency and returns the clarity of the radio station.
    """
    clarities = [check_clarity(frequency) for frequency in frequencies]
    initial_frequency = frequencies[0]
    fine_tuned_frequency = finetune_radio_station(initial_frequency, check_clarity)

    fig, ax = plt.subplots()
    ax.plot(frequencies, clarities)
    # Mark initial frequency
    initial_point = ax.plot(initial_frequency, clarities[initial_frequency - frequencies[0]], marker='o', color='red')
    initial_text = ax.text(
        initial_frequency,
        clarities[np.where(frequencies == initial_frequency)[0][0]],
        f'Initial: {initial_frequency}',
        fontsize=12)
    # Mark fine-tuned frequency
    fine_tuned_point = ax.plot(fine_tuned_frequency, clarities[fine_tuned_frequency - frequencies[0]], marker='o', color='green')
    fine_tuned_text = ax.text(
        fine_tuned_frequency,
        clarities[np.where(frequencies == fine_tuned_frequency)[0][0]],
        f'Fine-tuned: {fine_tuned_frequency}',
        fontsize=12)
    ax.set_xlabel('Frequency')
    ax.set_ylabel('Clarity')
    ax.set_title('Radio Station Clarity')
    ax.set_ylim(0, 120)
    ax.grid()

    def update(step: int):
        initial_frequency = frequencies[step]
        fine_tuned_frequency = finetune_radio_station(initial_frequency, check_clarity)
        # Update initial frequency
        initial_point[0].set_data([initial_frequency], [clarities[step]])
        initial_text.set_position((initial_frequency, clarities[step]))
        initial_text.set_text(f'Initial: {initial_frequency}')
        # Update fine-tuned frequency
        fine_tuned_point[0].set_data([fine_tuned_frequency], [clarities[fine_tuned_frequency - frequencies[0]]])
        fine_tuned_text.set_position((fine_tuned_frequency, clarities[fine_tuned_frequency - frequencies[0]]))
        fine_tuned_text.set_text(f'Fine-tuned: {fine_tuned_frequency}')
        return initial_point[0], initial_text, fine_tuned_point[0], fine_tuned_text

    step = len(frequencies) // 25
    anim = FuncAnimation(fig, update, frames=list(range(len(frequencies)))[::step], blit=True)  # noqa: F841
    plt.show()


if __name__ == '__main__':
    spectrum_version = 1

    if spectrum_version == 1:
        spectrum = TriangleSpectrum()
    elif spectrum_version == 2:
        spectrum = DoubleSinSpectrum()
    else:
        spectrum = TripleSinSpectrum()

    frequencies = np.arange(spectrum.left_edge, spectrum.right_edge + 1)
    draw_plot(frequencies, spectrum.check_clarity)
