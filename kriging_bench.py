from diagram_creator import sort_dimensions, create_chart, read_from_csv
from smt.surrogate_models import KRG
import egobox as egx
import numpy as np
import timeit
import time
import csv

start = time.time()
xt = np.array([[0.0, 1.0, 2.0, 3.0, 4.0]]).T
yt = np.array([[0.0, 1.0, 1.5, 0.9, 1.0]]).T
DIMENSIONS = [5, 10, 20, 100, 200, 500]
# NB_POINTS = [10, 13, 15]
NB_POINTS = [10, 50, 100, 250, 500, 1000]
NB_ITER = 5
LIBRARIES = ["SMT", "EGOBOX"]
CSV_filename = "kriging.csv"
file = True


def kriging_smt(num_points):
    sm = KRG(theta0=[1e-2])
    sm.set_training_values(xt, yt)
    sm.train()
    x = np.linspace(0.0, 4.0, num_points)
    y = sm.predict_values(x)
    s2 = sm.predict_variances(x)
    return y, s2


def kriging_egobox(num_points):
    gpx = egx.GpMix().fit(xt, yt)
    x = np.linspace(0.0, 4.0, num_points).reshape((-1, 1))
    y = gpx.predict_values(x)
    s2 = gpx.predict_variances(x)
    return y, s2


ALGOS = {"SMT": kriging_smt, "EGOBOX": kriging_egobox}


def run_benchmark(LIBRARIES):
    result = []
    for lib in LIBRARIES:
        for dim in DIMENSIONS:
            xlimits = np.full((dim, 2), [0, 1])
            for num_points in NB_POINTS:
                print(
                    f"Running benchmark with {lib} for {xlimits.shape} and {num_points} points"
                )
                time = timeit.timeit(lambda: ALGOS[lib](num_points), number=NB_ITER)
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
    write_to_csv(CSV_filename, run_benchmark(LIBRARIES))
    read_from_csv(CSV_filename)
    create_chart(sort_dimensions(), file)
    print(f"{time.time() - start} seconds")
