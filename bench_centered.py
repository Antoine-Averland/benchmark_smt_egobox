from benchmark import run_benchmark, write_to_csv
from diagram_creator import sort_dimensions, create_chart, read_from_csv
from smt.sampling_methods import LHS
import egobox as egx
import time

start = time.time()
LIBRARIES = ["SMT", "EGOBOX"]
data = {"SMT": {}, "EGOBOX": {}}
# NB_POINTS = [10, 50, 100, 250, 500, 1000]
NB_POINTS = [10, 13, 15]


def smt_lhs_centered(xlimits, num_points):
    sampling = LHS(xlimits=xlimits, criterion="center")
    sampling(num_points)


def egobox_lhs_centered(xlimits, num_points):
    xspecs = egx.to_specs(xlimits)
    egx.sampling(egx.Sampling.LHS_CENTERED, xspecs, num_points)


ALGOS = {"SMT": smt_lhs_centered, "EGOBOX": egobox_lhs_centered}

if __name__ == "__main__":
    write_to_csv("results_benchmark_centered.csv", run_benchmark(LIBRARIES, ALGOS))
    read_from_csv("results_benchmark_centered.csv")
    create_chart(sort_dimensions())
    print(f"{time.time() - start} seconds")
