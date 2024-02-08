"""
Author: Antoine Averland <antoine.averland@onera.fr>
create files with a bar chart for the comparisons.
"""

import csv
import matplotlib.pyplot as plt
import numpy as np


def create_chart(matrix_dimensions, list_num_points, data):
    for npoints in list_num_points:
        fig, ax = plt.subplots()
        bar_width = 0.35

        for i, program in enumerate(["SMT", "EGObox"]):
            matrix_means = [
                np.mean(data[program][matrix][npoints]) for matrix in matrix_dimensions
            ]
            matrix_stddevs = [
                np.std(data[program][matrix][npoints]) for matrix in matrix_dimensions
            ]

            ax.bar(
                np.arange(len(matrix_dimensions)) + i * bar_width,
                matrix_means,
                yerr=matrix_stddevs,
                width=bar_width,
                label=program,
            )

        ax.set_xticks(np.arange(len(matrix_dimensions)) + bar_width / 2)
        ax.set_xticklabels(matrix_dimensions)
        ax.set_xlabel("Matrix Dimensions")
        ax.set_ylabel("Average Time (seconds)")
        ax.set_title(f"Comparison for {npoints} Points")
        ax.legend()

        plt.savefig(f"comparison_{npoints}_points.png")
        plt.show()


if __name__ == "__main__":
    csv_filename = "results_benchmark.csv"

    data = {"SMT": {}, "EGObox": {}}

    with open(csv_filename, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            program = row["Program"]
            matrix = row["Matrix"]
            num_points = int(row["Num_Points"])
            average_time = float(row["Average_Time_(seconds)"])

            if matrix not in data[program]:
                data[program][matrix] = {}

            if num_points not in data[program][matrix]:
                data[program][matrix][num_points] = []

            data[program][matrix][num_points].append(average_time)

    matrix_dimensions = list(set(data["SMT"].keys()))
    list_num_points = [10, 50, 100, 250, 500, 1000]

    create_chart(matrix_dimensions, list_num_points, data)
