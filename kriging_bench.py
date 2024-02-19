from smt.problems import Sphere
from smt.surrogate_models import KRG
import egobox as egx
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
CSV_filename = "kriging.csv"
SMT_VERSION = "SMT_2.3.0"
EGOBOX_VERSION = "EGOBOX_0.15.1"
LIBRARIES = [SMT_VERSION, EGOBOX_VERSION]


def problem_smt(ndim, num):
    problem = Sphere(ndim=ndim)
    x = np.ones((num, ndim))
    x[:, 0] = np.linspace(-10, 10.0, num)
    x[:, 1] = 0.0
    y = problem(x)
    print(y.shape)
    return x, y


def kriging_smt(xt, yt):
    sm = KRG(theta0=[1e-2])
    sm.set_training_values(xt, yt)
    sm.train()


def kriging_egobox(xt, yt):
    egx.GpMix().fit(xt, yt)


ALGOS = {SMT_VERSION: kriging_smt, EGOBOX_VERSION: kriging_egobox}


def run_benchmark():
    result = []
    for lib in LIBRARIES:
        for dim in DIMENSIONS:
            for num_points in NB_POINTS:
                print(f"Running benchmark with {lib} for {dim} and {num_points} points")
                xt, yt = problem_smt(dim, num_points)
                time = timeit.timeit(lambda: ALGOS[lib](xt, yt), number=NB_ITER)
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


if __name__ == "__main__":
    write_to_csv(CSV_filename, run_benchmark())
    print(f"{time.time() - start} seconds")
