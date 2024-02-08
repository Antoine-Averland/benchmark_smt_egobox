from smt.sampling_methods import LHS
import egobox as egx
import numpy as np
import timeit
import csv

DIMENSIONS = [5]  # , 10, 20, 100]
NB_POINTS = [10]  # , 13, 15]
NB_ITER = 5
LIBRARIES = ["SMT", "EGOBOX"]


def smt_lhs(xlimits, num_points):
    sampling = LHS(xlimits=xlimits, criterion="ese", random_state=42)
    sampling(num_points)


def egobox_lhs(xlimits, num_points):
    xspecs = egx.to_specs(xlimits)
    egx.lhs(xspecs, num_points)


ALGOS = {"SMT": smt_lhs, "EGOBOX": egobox_lhs}


def run_benchmark():
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


if __name__ == "__main__":
    write_to_csv("results_benchmark2.csv", run_benchmark())
