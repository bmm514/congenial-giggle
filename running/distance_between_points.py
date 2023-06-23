#Script to calcualte the average distance between a set of points

#Start by doing brute force by generating 1000 combinations then getting average

import numpy
import random

def get_distance(x,y, distance_matrix):
    return distance_matrix[x-1,y-1]

def update_min_max(min_max, total_distance):
    if total_distance < min_max[0]:
        min_max[0] = total_distance
    if total_distance > min_max[1]:
        min_max[1] = total_distance

    return min_max

def calculate_distance(distance_matrix, point_order):
    total_distance = 0
    for i in range(len(point_order) - 1):
        start, end = point_order[i], point_order[i+1]
        total_distance += get_distance(start, end, distance_matrix)

    total_distance += get_distance(point_order[-1], point_order[0], distance_matrix)

    return total_distance

def main():
    distance_matrix = numpy.array([
        [0.00,2.30,2.00,1.10,2.08,5.90],
        [2.30,0.00,2.38,2.94,4.17,6.92], 
        [2.00,2.38,0.00,3.13,2.59,4.54], 
        [1.10,2.94,3.13,0.00,2.52,6.77],
        [2.08,4.17,2.59,2.52,0.00,4.47],
        [5.90,6.92,4.54,6.77,4.77,0.00]
        ])

    point_order = [2,3,4,5,6]
    iterations = 10000000

    predicted_total_distance = 0
    min_max = [numpy.inf, 0]
    for i in range(iterations):
        random.shuffle(point_order)
        start_point_order = [1] + point_order
        total_distance = calculate_distance(distance_matrix, start_point_order)
        min_max = update_min_max(min_max, total_distance)
        predicted_total_distance += total_distance

    print(start_point_order, total_distance)
    predicted_distance = predicted_total_distance / iterations

    expected_distance = distance_matrix.sum() / (len(start_point_order) - 1)

    return predicted_distance, expected_distance, min_max

if __name__ == '__main__':
    predicted_distance, expected_distance, min_max = main()  
    print(predicted_distance)
    print(expected_distance)
    print(min_max)
