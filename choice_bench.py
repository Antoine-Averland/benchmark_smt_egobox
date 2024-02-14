from functions import (
    smt_lhs_opti,
    egobox_lhs_opti,
    smt_lhs_classic,
    egobox_lhs_classic,
    smt_lhs_centered,
    egobox_lhs_centered,
    smt_lhs_maximin,
    egobox_lhs_maximin,
    smt_lhs_centered_maximin,
    egobox_lhs_centered_maximin,
)
from benchmark import run_benchmark, write_to_csv
from diagram_creator import sort_dimensions, create_chart, read_from_csv
import argparse
import time

start = time.time()
ALGOS = {}
LIBRARIES = ["SMT", "EGOBOX"]
CSV_filename = "results_bench.csv"
file = False


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run benchmark for different functions."
    )
    parser.add_argument(
        "--lhs",
        choices=["opti", "classic", "centered", "maximin", "centered_maximin"],
        default="classic",
        help="Specify the choice of the type of lhs",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    if args.lhs == "opti":
        ALGOS = {"SMT": smt_lhs_opti, "EGOBOX": egobox_lhs_opti}
    elif args.lhs == "classic":
        ALGOS = {"SMT": smt_lhs_classic, "EGOBOX": egobox_lhs_classic}
    elif args.lhs == "centered":
        ALGOS = {"SMT": smt_lhs_centered, "EGOBOX": egobox_lhs_centered}
    elif args.lhs == "maximin":
        ALGOS = {"SMT": smt_lhs_maximin, "EGOBOX": egobox_lhs_maximin}
    elif args.lhs == "centered_maximin":
        ALGOS = {
            "SMT": smt_lhs_centered_maximin,
            "EGOBOX": egobox_lhs_centered_maximin,
        }

    write_to_csv(CSV_filename, run_benchmark(LIBRARIES, ALGOS))
    read_from_csv(CSV_filename)
    create_chart(sort_dimensions(), file)
    print(f"{time.time() - start} seconds")
