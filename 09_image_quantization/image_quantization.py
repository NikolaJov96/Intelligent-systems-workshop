from math import sqrt
from random import randint
from typing import List, Tuple

import cv2
import matplotlib.pyplot as plt


def k_means(dataset: List[Tuple], k: int, tries: int) -> Tuple[List[Tuple], int]:
    """
    Executes the k-means algorithm on the given dataset and returns the centroids.
    The dataset is in the form of a list of tuples, where each tuple represents a
    N-dimensional point that is to be clustered.

    Params:
    -------
    dataset: List[Tuple]
        The dataset to be clustered.
    k: int
        The number of clusters.
    tries: int
        The number of times the algorithm will be executed to find the best centroids.

    Returns:
    --------
    List[Tuple]
        The centroids of the clusters.
    int
        The variation of the clusters.
    """
    pass


if __name__ == '__main__':
    image = cv2.imread('image.jpg')
    height, width, _ = image.shape
    display_height = 600
    if height > display_height:
        image = cv2.resize(image, (int(width * display_height / height), display_height))
    dataset_image_height = 50
    if height > dataset_image_height:
        dataset_image = cv2.resize(image, (int(width * dataset_image_height / height), dataset_image_height))

    cv2.imshow('Original Image', image)
    cv2.waitKey(100)

    dataset = []
    for i in range(dataset_image.shape[0]):
        for j in range(dataset_image.shape[1]):
            dataset.append((dataset_image[i, j, 0], dataset_image[i, j, 1], dataset_image[i, j, 2]))

    min_k = 2
    max_k = 9
    variations = []
    for k in range(min_k, max_k + 1):
        centroids, variation = k_means(dataset, k, tries=5)
        variations.append(variation)
        quantized_image = image.copy()
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                min_distance = float('inf')
                min_centroid = None
                for centroid in centroids:
                    distance = sum((image[i, j] - centroid) ** 2)
                    if distance < min_distance:
                        min_distance = distance
                        min_centroid = centroid
                quantized_image[i, j] = min_centroid
        cv2.imshow(f'Quantized Image (k={k})', quantized_image)
        cv2.waitKey(100)

    plt.plot(range(min_k, max_k + 1), variations)
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Variation')
    plt.title('Variation vs Number of Clusters')
    plt.show()

    cv2.waitKey(0)
    cv2.destroyAllWindows()
