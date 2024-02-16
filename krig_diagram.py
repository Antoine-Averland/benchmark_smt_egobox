import csv
import matplotlib.pyplot as plt
import numpy as np

data = {"SMT_2.3.0": {}}
# NB_POINTS = [10, 50, 100, 250, 500, 1000]
NB_POINTS = [10, 13, 15]


def sort_dimensions():
    matrix_dimensions = list(set(data["SMT_2.3.0"].keys()))
    nb_matrix = [int(dim) for dim in matrix_dimensions]
    sort_matrix = sorted(nb_matrix)
    sort_matrix_str = [str(number) for number in sort_matrix]
    print(sort_matrix_str)
    return sort_matrix_str


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


def create_chart(matrix_dimensions):
    num_points = len(NB_POINTS)
    bar_width = 0.2
    total_width = num_points * bar_width
    gap = 0.2

    for i, npoints in enumerate(NB_POINTS):
        matrix = [data["SMT_2.3.0"][matrix][npoints] for matrix in matrix_dimensions]

        plt.bar(
            np.arange(len(matrix_dimensions)) * bar_width + total_width,
            matrix,
            width=bar_width,
            label="SMT_2.3.0",
        )

        plt.xlabel("Dimensions of x")
        plt.ylabel("Average Time (seconds)")
        plt.title(f"kriging - {npoints} points")
        plt.xticks(
            np.arange(len(matrix_dimensions)) * (total_width + gap)
            + (total_width - bar_width) / 2,
            matrix_dimensions,
        )
        plt.legend()

        plt.savefig(f"results/kriging/results_krig_{npoints}_points.png")
        plt.show()


if __name__ == "__main__":
    read_from_csv("kriging.csv")
    create_chart(sort_dimensions())
