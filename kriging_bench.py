from smt.problems import Sphere
import numpy as np
import timeit
import time
import csv

start = time.time()
# DIMENSIONS = [5, 10, 20, 100, 200, 500]
DIMENSIONS = [5, 10]
NB_POINTS = [10, 13, 15]
# NB_POINTS = [10, 50, 100, 250, 500, 1000]
NB_ITER = 5
LIBRARIES = "SMT_2.3.0"
CSV_filename = "kriging.csv"
file = True


def kriging_smt():
    for ndim in DIMENSIONS:
        problem = Sphere(ndim=ndim)
        for num in NB_POINTS:
            x = np.ones((num, ndim))
            x[:, 0] = np.linspace(-10, 10.0, num)
            x[:, 1] = 0.0
            y = problem(x)

            yd = np.empty((num, ndim))
            for i in range(ndim):
                yd[:, i] = problem(x, kx=i).flatten()

            print(y.shape)
            print(yd.shape)


ALGOS = {"SMT": kriging_smt}


def run_benchmark():
    result = []
    for dim in DIMENSIONS:
        xlimits = np.full((dim, 2), [0, 1])
        for num_points in NB_POINTS:
            print(f"Running benchmark for {xlimits.shape} and {num_points} points")
            time = timeit.timeit(lambda: kriging_smt(), number=NB_ITER)
            res = {
                "lib": LIBRARIES,
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


if __name__ == "__main__":
    write_to_csv(CSV_filename, run_benchmark())
    print(f"{time.time() - start} seconds")
