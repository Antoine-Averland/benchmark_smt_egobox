from benchmark import run_benchmark, write_to_csv
from smt.sampling_methods import LHS
from diagram_creator import sort_dimensions, create_chart, read_from_csv
import egobox as egx
import time

start = time.time()
LIBRARIES = ["SMT", "EGOBOX"]
data = {"SMT": {}, "EGOBOX": {}}
# NB_POINTS = [10, 50, 100, 250, 500, 1000]
NB_POINTS = [10, 13, 15]


def smt_lhs_opti(xlimits, num_points):
    sampling = LHS(xlimits=xlimits, criterion="ese", random_state=42)
    sampling(num_points)


def egobox_lhs_opti(xlimits, num_points):
    xspecs = egx.to_specs(xlimits)
    egx.lhs(xspecs, num_points)


ALGOS = {"SMT": smt_lhs_opti, "EGOBOX": egobox_lhs_opti}

if __name__ == "__main__":
    write_to_csv("results_benchmark_optimized.csv", run_benchmark(LIBRARIES, ALGOS))
    read_from_csv("results_benchmark_optimized.csv")
    create_chart(sort_dimensions())
    print(f"{(time.time() - start) / 60} minutes")
