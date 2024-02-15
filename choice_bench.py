#   from functions import (
#       smt_lhs,
#       # smt_lhs_opti,
#       egobox_lhs_opti,
#       # smt_lhs_classic,
#       egobox_lhs_classic,
#       smt_lhs_centered,
#       egobox_lhs_centered,
#       smt_lhs_maximin,
#       egobox_lhs_maximin,
#       smt_lhs_centered_maximin,
#       egobox_lhs_centered_maximin,
#   )
#   from benchmark import run_benchmark, write_to_csv
#   import argparse
#   import time
#
#   start = time.time()
#   ALGOS = {}
#   LIBRARIES = ["SMT_2.3.0", "EGOBOX_0.15.1"]
#
#
#   def parse_arguments():
#       parser = argparse.ArgumentParser(
#           description="Run benchmark for different functions."
#       )
#       parser.add_argument(
#           "--lhs",
#           choices=["opti", "classic", "centered", "maximin", "centered_maximin"],
#           default="classic",
#           help="Specify the choice of the type of lhs",
#       )
#       return parser.parse_args()
#
#
#   if __name__ == "__main__":
#       args = parse_arguments()
#
#       if args.lhs == "opti":
#           ALGOS = {"SMT_2.3.0": smt_lhs, "EGOBOX_0.15.1": egobox_lhs_opti}
#           CSV_filename = "results_opti.csv"
#       elif args.lhs == "classic":
#           ALGOS = {"SMT_2.3.0": smt_lhs, "EGOBOX_0.15.1": egobox_lhs_classic}
#           CSV_filename = "results_classic.csv"
#       elif args.lhs == "centered":
#           ALGOS = {"SMT_2.3.0": smt_lhs_centered, "EGOBOX_0.15.1": egobox_lhs_centered}
#           CSV_filename = "results_centered.csv"
#       elif args.lhs == "maximin":
#           ALGOS = {"SMT_2.3.0": smt_lhs_maximin, "EGOBOX_0.15.1": egobox_lhs_maximin}
#           CSV_filename = "results_maximin.csv"
#       elif args.lhs == "centered_maximin":
#           ALGOS = {
#               "SMT_2.3.0": smt_lhs_centered_maximin,
#               "EGOBOX_0.15.1": egobox_lhs_centered_maximin,
#           }
#           CSV_filename = "results_centered_maximin.csv"
#
#       write_to_csv(CSV_filename, run_benchmark(LIBRARIES, ALGOS))
#       print(f"{time.time() - start} seconds")
