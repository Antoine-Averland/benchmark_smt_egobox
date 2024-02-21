import csv
import matplotlib.pyplot as plt
import numpy as np

SMT_VERSION = "SMT_2.3.0"
EGOBOX_VERSION = "EGOBOX_0.15.1"
# data = {SMT_VERSION: {}, EGOBOX_VERSION: {}}
NB_POINTS = [10, 50, 100, 250, 500, 1000]
LHS_OPTION_NAMES = ["optimized", "classic", "centered", "maximin", "centered_maximin"]


def sort_dimensions(data):
    matrix_dimensions = list(set(data[SMT_VERSION].keys()))
    nb_matrix = [int(dim) for dim in matrix_dimensions]
    sort_matrix = sorted(nb_matrix)
    sort_matrix_str = [str(number) for number in sort_matrix]
    return sort_matrix_str


def create_chart(lhs_option, dimensions, data):
    fig, axs = plt.subplots(2, 3, figsize=(15, 8))
    fig.suptitle(f"LHS {lhs_option}")

    for i, npoints in enumerate(NB_POINTS):
        row, col = divmod(i, 3)

        for j, program in enumerate([SMT_VERSION, EGOBOX_VERSION]):
            matrix_values = [data[program][matrix][npoints] for matrix in dimensions]

            axs[row, col].bar(
                np.arange(len(dimensions)) + j * 0.35,
                matrix_values,
                width=0.35,
                label=program,
            )

        axs[row, col].set_xticks(np.arange(len(dimensions)))
        axs[row, col].set_xticklabels(dimensions)
        axs[row, col].set_xlabel("Dimensions of x")
        axs[row, col].set_ylabel("time")
        axs[row, col].set_title(f"{npoints} points")
        axs[row, col].legend()

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(f"results/lhs_{lhs_option}/LHS_{lhs_option}_benchmarks.png")
    plt.close()


def read_from_csv(csv_filename):
    data = {SMT_VERSION: {}, EGOBOX_VERSION: {}}
    with open(csv_filename, mode="r") as file:
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
    return data


if __name__ == "__main__":
    for lhs_type in LHS_OPTION_NAMES:
        csv_filename = f"results_{lhs_type}.csv"
        print(lhs_type)
        data = read_from_csv(csv_filename)
        dimensions = sort_dimensions(data)
        create_chart(lhs_type, dimensions, data)
