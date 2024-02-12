import numpy as np
import timeit
import csv

DIMENSIONS = [5, 10, 20, 100, 200, 500]
NB_POINTS = [10, 13, 15]
# NB_POINTS = [10, 50, 100, 250, 500, 1000]
NB_ITER = 5


def run_benchmark(LIBRARIES, ALGOS):
    result = []
    for lib in LIBRARIES:
        for dim in DIMENSIONS:
            xlimits = np.full((dim, 2), [0, 1])
            for num_points in NB_POINTS:
                print(
                    f"Running benchmark with {lib} for {xlimits.shape} and {num_points} points"
                )
                time = timeit.timeit(
                    lambda: ALGOS[lib](xlimits, num_points), number=NB_ITER
                )
                res = {
                    "lib": lib,
                    "dim": dim,
                    "nb_points": num_points,
                    "time": time / NB_ITER,
                }
                print(res)
                result.append(res)
    return result


def write_to_csv(csv_filename, result):
    with open(csv_filename, mode="w", newline="") as csvfile:
        headers = result[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        for line in result:
            writer.writerow(line)
