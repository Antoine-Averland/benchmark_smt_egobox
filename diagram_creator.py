from benchmark import parse_arguments
import csv
import matplotlib.pyplot as plt
import numpy as np


data = {"SMT_2.3.0": {}, "EGOBOX_0.15.1": {}}
# NB_POINTS = [10, 50, 100, 250, 500, 1000]
NB_POINTS = [10, 13, 15]
file = False


def sort_dimensions():
    matrix_dimensions = list(set(data["SMT_2.3.0"].keys()))
    nb_matrix = [int(dim) for dim in matrix_dimensions]
    sort_matrix = sorted(nb_matrix)
    sort_matrix_str = [str(number) for number in sort_matrix]
    print(sort_matrix_str)
    return sort_matrix_str


def create_chart(matrix_dimensions, file, lhs):
    for npoints in NB_POINTS:
        fig, ax = plt.subplots()
        bar_width = 0.35

        for i, program in enumerate(["SMT_2.3.0", "EGOBOX_0.15.1"]):
            matrix = [data[program][matrix][npoints] for matrix in matrix_dimensions]

            ax.bar(
                np.arange(len(matrix_dimensions)) + i * bar_width,
                matrix,
                width=bar_width,
                label=program,
            )

        ax.set_xticks(np.arange(len(matrix_dimensions)) + bar_width / 2)
        ax.set_xticklabels(matrix_dimensions)
        ax.set_xlabel("Dimensions of x")
        ax.set_ylabel("Average Time (seconds)")
        if file:
            ax.set_title(f"kriging - {npoints} points")
        else:
            ax.set_title(f"LHS {lhs} - {npoints} points")
        ax.legend()

        plt.savefig(f"results/lhs_{lhs}/LHS_{lhs}_{npoints}_points.png")


def read_from_csv(CSV_filename):
    with open(CSV_filename, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            program = row["lib"]
            matrix = row["dim"]
            num_points = int(row["nb_points"])
            average_time = float(row["time"])

            if matrix not in data[program]:
                data[program][matrix] = {}

            if num_points not in data[program][matrix]:
                data[program][matrix][num_points] = average_time


if __name__ == "__main__":
    args = parse_arguments()
    csv_filename = f"results_{args.lhs}.csv"
    print(args.lhs)

    read_from_csv(csv_filename)
    create_chart(sort_dimensions(), file, args.lhs)
