from math import sqrt
from typing import List, Tuple

import matplotlib.pyplot as plt
from cyclist_dataset import BicycleSize, Cyclist, create_bicycle_dataset, plot_bicycle_dataset


def knn(dataset: List[Tuple[Cyclist, BicycleSize]], k: int, cyclist: Cyclist) -> BicycleSize:
    """
    Predicts the bicycle size of a cyclist using the k-Nearest Neighbors algorithm.

    Parameters
    ----------
    dataset : List[Tuple[Cyclist, BicycleSize]]
        The dataset of cyclists with their respective bicycle sizes.
    k : int
        The number of neighbors to consider.
    cyclist : Cyclist
        The cyclist to predict the bicycle size for.

    Returns
    -------
    BicycleSize
        The predicted bicycle size.
    """
    pass


def find_best_k(dataset: List[Tuple[Cyclist, BicycleSize]]) -> Tuple[int, List[float]]:
    """
    Finds the best k for the k-Nearest Neighbors algorithm using the dataset.
    Also returns the percentage of correct predictions for each k.

    Parameters
    ----------
    dataset : List[Tuple[Cyclist, BicycleSize]]
        The dataset of cyclists with their respective bicycle sizes.

    Returns
    -------
    int
        The best k for the k-Nearest Neighbors algorithm.
    List[float]
        The percentage of correct predictions for each k.
    """
    pass


if __name__ == '__main__':
    # Generate the cyclist dataset and a cyclist
    dataset = create_bicycle_dataset(100)
    cyclist = Cyclist(172, 86, 75)

    # Plot the dataset with the cyclist
    plot_bicycle_dataset(dataset, 'Bicycle dataset', cyclist)

    # Predict the bicycle size for a cyclist for different k
    predicted_sizes = []
    for k in range(1, len(dataset) + 1):
        predicted_size = knn(dataset, k, cyclist)
        predicted_sizes.append(predicted_size)

    # Plot relation between k and predicted sizes
    plt.plot(range(1, len(dataset) + 1), [bike_size.value for bike_size in predicted_sizes])
    plt.xlabel('K')
    plt.ylabel('Bicycle size')
    plt.yticks([bike_size.value for bike_size in BicycleSize], [bike_size.name for bike_size in BicycleSize])
    plt.title('Predicted bicycle size per K')
    plt.show()

    # Plot the histogram of the predicted sizes without using plt.hist
    plt.bar([bike_size.value for bike_size in BicycleSize], [predicted_sizes.count(bike_size) for bike_size in BicycleSize])
    plt.xlabel('Bicycle size')
    plt.xticks([bike_size.value for bike_size in BicycleSize], [bike_size.name for bike_size in BicycleSize])
    plt.ylabel('Count')
    plt.title('Predicted bicycle sizes')
    plt.show()

    # Find and plot the best k for various dataset standard variation scales
    for variation_scale in [0.04, 0.2, 1.0, 5.0, 25.0]:
        dataset = create_bicycle_dataset(100, variation_scale)
        plot_bicycle_dataset(dataset, f'Bicycle dataset (deviation scale: {variation_scale})', cyclist)
        k, correct_per_k = find_best_k(dataset)
        plt.plot(range(1, len(dataset) + 1), correct_per_k)
        plt.axvline(x=k, color='r', linestyle='--')
        plt.text(k + 1, 5, f'Best K: {k}', color='r')
        plt.ylim(-5, 105)
        plt.xlabel('K')
        plt.ylabel('Correct predictions (%)')
        plt.title(f'Correct predictions per K (deviation scale: {variation_scale})')
        plt.show()
