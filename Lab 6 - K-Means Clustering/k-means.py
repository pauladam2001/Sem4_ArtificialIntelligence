import csv
from cmath import sqrt
from random import random

import numpy as np
from matplotlib import pyplot


def readPoints(file_name):
    points = dict()
    with open(file_name, "r") as file:
        file.readline()
        while line := file.readline()[:-1]:
            tokens = line.split(",")
            points[(float(tokens[1]), float(tokens[2]))] = tokens[0]
    return points


def distance(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def get_closest_centroid(centroids, point):
    sol = centroids[0]
    for centroid in centroids[1:]:
        if np.absolute(distance(centroid, point)) < np.absolute(distance(sol, point)):
            sol = centroid
    return sol


def new_centroids(points, k):
    minX = min([point[0] for point in points])
    maxX = max([point[0] for point in points])
    minY = min([point[1] for point in points])
    maxY = max([point[1] for point in points])

    centroids = [[0, 0] for _ in range(k)]
    centroid_cnt = [0 for _ in range(k)]
    for point in points:
        centroid_cnt[points[point]] += 1
        centroid = centroids[points[point]]
        centroid[0] += point[0]
        centroid[1] += point[1]

    # new centroid cj=mean of all points assigned to cluster j in the previous step
    sol = []
    for i, centroid in enumerate(centroids):
        if centroid_cnt[i] != 0:
            sol.append((centroid[0] / centroid_cnt[i], centroid[1] / centroid_cnt[i]))
        else:
            sol.append((random() * (maxX - minX) + minX, random() * (maxY - minY) + minY))
    return sol


def solve(points, k):
    sol = dict()
    minX = min([point[0] for point in points])
    maxX = max([point[0] for point in points])
    minY = min([point[1] for point in points])
    maxY = max([point[1] for point in points])
    centroids = []
    for _ in range(k):  # select 4 random centroids
        centroids.append((random() * (maxX - minX) + minX, random() * (maxY - minY) + minY))
    nrIterations = 1000
    for i in range(nrIterations):  # search for all the points the closest centroid to it
        for point in points:
            centroid = get_closest_centroid(centroids, point)
            sol[point] = centroids.index(centroid)  # assign the point to a cluster
        if i != nrIterations - 1:
            centroids = new_centroids(sol, k)  # run again through all the points and recompute their positions
    return sol, centroids  # stop when none of the cluster assignments changed


def compute_statistics(points, data):
    true_positive = true_negative = false_negative = false_positive = 0
    for i, p in enumerate(points):
        if points[p] == 0:
            if data[p] == 'A':
                true_positive += 1
            else:
                false_positive += 1
        else:
            if data[p] != 'A':
                true_negative += 1
            else:
                false_negative += 1
    accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_negative + false_positive)
    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
    score = 2 * precision * recall / (precision + recall)
    print("A")
    print("accuracy: " + str(accuracy))
    print("precision: " + str(precision))
    print("recall: " + str(recall))
    print("score: " + str(score))

    for i, p in enumerate(points):
        if points[p] == 1:
            if data[p] == 'B':
                true_positive += 1
            else:
                false_positive += 1
        else:
            if data[p] != 'B':
                true_negative += 1
            else:
                false_negative += 1
    accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_negative + false_positive)
    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
    score = 2 * precision * recall / (precision + recall)
    print("B")
    print("accuracy: " + str(accuracy))
    print("precision: " + str(precision))
    print("recall: " + str(recall))
    print("score: " + str(score))

    for i, p in enumerate(points):
        if points[p] == 2:
            if data[p] == 'C':
                true_positive += 1
            else:
                false_positive += 1
        else:
            if data[p] != 'C':
                true_negative += 1
            else:
                false_negative += 1
    accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_negative + false_positive)
    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
    score = 2 * precision * recall / (precision + recall)
    print("C")
    print("accuracy: " + str(accuracy))
    print("precision: " + str(precision))
    print("recall: " + str(recall))
    print("score: " + str(score))

    for i, p in enumerate(points):
        if points[p] == 0:
            if data[p] == 'D':
                true_positive += 1
            else:
                false_positive += 1
        else:
            if data[p] != 'D':
                true_negative += 1
            else:
                false_negative += 1
    accuracy = (true_positive + true_negative) / (true_positive + true_negative + false_negative + false_positive)
    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
    score = 2 * precision * recall / (precision + recall)
    print("D")
    print("accuracy: " + str(accuracy))
    print("precision: " + str(precision))
    print("recall: " + str(recall))
    print("score: " + str(score))


if __name__ == "__main__":
    # load data
    data = readPoints("dataset.csv")
    colors = ["brown", "yellow", "green", "black"]

    k = 4
    points, centroids = solve(data, k)

    compute_statistics(points, data)

    for point in points:
        pyplot.scatter(point[0], point[1], color=colors[points[point]])
    for point in centroids:
        pyplot.scatter(point[0], point[1], color="blue")
    pyplot.show()
