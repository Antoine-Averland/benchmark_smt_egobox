import argparse
import numpy as np
import timeit
import csv
import time
from smt.sampling_methods import LHS
import egobox as egx

# DIMENSIONS = [5, 10, 20, 100, 200, 500]
DIMENSIONS = [5, 10]
NB_POINTS = [10, 13, 15]
# NB_POINTS = [10, 50, 100, 250, 500, 1000]
NB_ITER = 20
SMT_VERSION = "SMT_2.3.0"
EGOBOX_VERSION = "EGOBOX_0.15.1"

LHS_OPTION_NAMES = ["optimized", "classic", "centered", "maximin", "centered_maximin"]

SMT_LHS_OPTIONS = {
    "classic": "c",
    "optimized": "ese",
    "centered": "center",
    "maximin": "maximin",
    "centered_maximin": "centermaximin",
}
EGOBOX_LHS_OPTIONS = {
    "classic": egx.Sampling.LHS_CLASSIC,
    "optimized": egx.Sampling.LHS,
    "centered": egx.Sampling.LHS_CENTERED,
    "maximin": egx.Sampling.LHS_MAXIMIN,
    "centered_maximin": egx.Sampling.LHS_CENTERED_MAXIMIN,
}


def smt_lhs(xlimits, num_points, lhs_opt):
    sampling = LHS(xlimits=xlimits, criterion=SMT_LHS_OPTIONS[lhs_opt])
    sampling(num_points)


def egobox_lhs(xlimits, num_points, lhs_opt):
    xspecs = egx.to_specs(xlimits)
    egx.sampling(EGOBOX_LHS_OPTIONS[lhs_opt], xspecs, num_points)


start = time.time()
ALGOS = {SMT_VERSION: smt_lhs, EGOBOX_VERSION: egobox_lhs}
LIBRARIES = [SMT_VERSION, EGOBOX_VERSION]


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run benchmark for different functions."
    )
    parser.add_argument(
        "--lhs",
        choices=LHS_OPTION_NAMES + ["all"],
        default="all",
        help="Specify the choice of the type of lhs",
    )
    return parser.parse_args()


def run_benchmark(lhs_option):
    result = []
    for lib in LIBRARIES:
        for dim in DIMENSIONS:
            xlimits = np.full((dim, 2), [0, 1])
            for num_points in NB_POINTS:
                print(
                    f"Running benchmark with {lib} {args.lhs} for {xlimits.shape} and {num_points} points"
                )
                time = timeit.timeit(
                    lambda: ALGOS[lib](xlimits, num_points, lhs_option), number=NB_ITER
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
        for lhs_type in LHS_OPTION_NAMES:
            csv_filename = f"results_{lhs_type}.csv"
            write_to_csv(csv_filename, run_benchmark(lhs_type))

    else:
        csv_filename = f"results_{args.lhs}.csv"
        write_to_csv(csv_filename, run_benchmark(args.lhs))

    print(f"{time.time() - start} seconds")
