import argparse
import numpy as np
import timeit
import csv
import time
from smt.sampling_methods import LHS
import egobox as egx

type_lhs = {
    "classic": "c",
    "opti": "ese",
    "centered": "center",
    "maximin": "maximin",
    "centered_maximin": "centermaximin",
}
type_ego = {
    "classic": egx.Sampling.LHS_CLASSIC,
    "opti": "",
    "centered": egx.Sampling.LHS_CENTERED,
    "maximin": egx.Sampling.LHS_MAXIMIN,
    "centered_maximin": egx.Sampling.LHS_CENTERED_MAXIMIN,
}


def smt_lhs(xlimits, num_points, args):
    sampling = LHS(xlimits=xlimits, criterion=type_lhs[args.lhs])
    sampling(num_points)


def egobox_lhs(xlimits, num_points, args):
    xspecs = egx.to_specs(xlimits)
    if args.lhs == "opti":
        egx.lhs(xspecs, num_points)
    else:
        egx.sampling(type_ego[args.lhs], xspecs, num_points)


# DIMENSIONS = [5, 10, 20, 100, 200, 500]
DIMENSIONS = [5, 10]
NB_POINTS = [10, 13, 15]
# NB_POINTS = [10, 50, 100, 250, 500, 1000]
NB_ITER = 20


start = time.time()
ALGOS = {}
LIBRARIES = ["SMT_2.3.0", "EGOBOX_0.15.1"]


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run benchmark for different functions."
    )
    parser.add_argument(
        "--lhs",
        choices=["opti", "classic", "centered", "maximin", "centered_maximin", "all"],
        default="all",
        help="Specify the choice of the type of lhs",
    )
    return parser.parse_args()


def run_benchmark(LIBRARIES, ALGOS):
    result = []
    for lib in LIBRARIES:
        for dim in DIMENSIONS:
            xlimits = np.full((dim, 2), [0, 1])
            for num_points in NB_POINTS:
                print(
                    f"Running benchmark with {lib} {args.lhs} for {xlimits.shape} and {num_points} points"
                )
                time = timeit.timeit(
                    lambda: ALGOS[lib](xlimits, num_points, args), number=NB_ITER
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
    args = parse_arguments()
    if args.lhs == "all":
        for lhs_type in type_lhs.keys():
            csv_filename = f"results_{lhs_type}.csv"
            ALGOS = {"SMT_2.3.0": smt_lhs, "EGOBOX_0.15.1": egobox_lhs}
            write_to_csv(csv_filename, run_benchmark(LIBRARIES, ALGOS))

    else:
        csv_filename = f"results_{args.lhs}.csv"
        ALGOS = {"SMT_2.3.0": smt_lhs, "EGOBOX_0.15.1": egobox_lhs}
        write_to_csv(csv_filename, run_benchmark(LIBRARIES, ALGOS))

    print(f"{time.time() - start} seconds")
