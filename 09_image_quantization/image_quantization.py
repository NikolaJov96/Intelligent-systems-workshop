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
    # Get the dimension of the dataset
    d = len(dataset[0])

    best_variations = [float('inf') for _ in range(k)]
    best_centroids = None

    for _ in range(tries):
        # Initialize the centroids randomly
        previous_centroids = [[randint(0, 255) for _ in range(d)] for _ in range(k)]

        while True:
            cluster_sums = [[0 for _ in range(d)] for _ in range(k)]
            cluster_counts = [0 for _ in range(k)]

            # Add each point to the sum of its assigned cluster
            for point_id in range(len(dataset)):
                min_distance = float('inf')
                min_centroid = None
                for cluster_id in range(k):
                    distance = 0
                    for i in range(d):
                        distance += (dataset[point_id][i] - previous_centroids[cluster_id][i]) ** 2
                    distance = sqrt(distance)
                    if distance < min_distance:
                        min_distance = distance
                        min_centroid = cluster_id
                for i in range(d):
                    cluster_sums[min_centroid][i] += dataset[point_id][i]
                cluster_counts[min_centroid] += 1

            # Update the centroids
            centroids = [[0 for _ in range(d)] for _ in range(k)]
            for cluster_id in range(k):
                for i in range(d):
                    centroids[cluster_id][i] = 0
                    if cluster_counts[cluster_id] > 0:
                        centroids[cluster_id][i] = int(cluster_sums[cluster_id][i] / cluster_counts[cluster_id])

            # Check for convergence
            if all(centroid in previous_centroids for centroid in centroids):
                break

            previous_centroids = centroids

        # Calculate the variation
        new_variations = [0 for _ in range(k)]
        for point_id in range(len(dataset)):
            min_distance = float('inf')
            min_cluster = 0
            for cluster_id in range(k):
                distance = 0
                for i in range(d):
                    distance += (dataset[point_id][i] - centroids[cluster_id][i]) ** 2
                if distance < min_distance:
                    min_distance = distance
                    min_cluster = cluster_id
            new_variations[min_cluster] += min_distance

        # Keep the centroids with the minimal highest variation
        if sum(new_variations) < sum(best_variations):
            best_variations = new_variations
            best_centroids = centroids

    return best_centroids, sum(best_variations)


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
