import csv
import matplotlib.pyplot as plt
import numpy as np
import argparse

SMT_VERSION = "SMT_2.4.0"
EGOBOX_VERSION = "EGOBOX_0.25.1"
# data = {SMT_VERSION: {}, EGOBOX_VERSION: {}}
CSV_FILENAME = f"results/kriging/kriging_{SMT_VERSION}_{EGOBOX_VERSION}.csv"
# NB_POINTS1 = [50, 200, 400]
NB_POINTS2 = [600, 1000]

NB_POINTS1 = [10, 13]
NB_POINTS2 = [15]



def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run benchmark for different functions."
    )
    parser.add_argument(
        "--dimensions",
        choices=["low", "high"],
        default="low",
        help="Specify the choice of the type of lhs",
    )
    return parser.parse_args()


def sort_dimensions(data, args):
    matrix_dimensions = list(set(data[SMT_VERSION].keys()))
    nb_matrix = [int(dim) for dim in matrix_dimensions]
    if args == "low":
        sort_matrix = sorted(nb_matrix)[:-2]
    elif args == "high":
        sort_matrix = sorted(nb_matrix)[-2:]
    sort_matrix_str = [str(number) for number in sort_matrix]
    print(sort_matrix_str)
    return sort_matrix_str


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


def create_chart(matrix_dimensions, data, nb_points, args):
    bar_width = 0.35
    index = np.arange(len(matrix_dimensions))
    print(index)

    smt_times = [
        data[SMT_VERSION][dim][num_points]
        for num_points, dim in zip(nb_points, matrix_dimensions)
    ]
    egobox_times = [
        data[EGOBOX_VERSION][dim][num_points]
        for num_points, dim in zip(nb_points, matrix_dimensions)
    ]
    print(smt_times)
    print(egobox_times)
    plt.bar(index, smt_times, width=bar_width, label=SMT_VERSION)
    plt.bar(
        index + bar_width,
        egobox_times,
        width=bar_width,
        label=EGOBOX_VERSION,
    )
    index = index + 2 * bar_width

    plt.xlabel("Dimensions")
    plt.ylabel("Temps (s)")
    plt.title(f"kriging {args} dimensions benchmark")
    plt.xticks(index - bar_width, matrix_dimensions)
    plt.legend()
    plt.savefig(f"results/kriging/kriging_{args}_dimensions_{SMT_VERSION}_{EGOBOX_VERSION}.png")


# def create_line_chart_kriging(matrix_dimensions, data, nb_points, args):
#     plt.figure(figsize=(10, 6))

#     smt_times = [
#         data[SMT_VERSION][dim][num_points]
#         for num_points, dim in zip(nb_points, matrix_dimensions)
#     ]
#     egobox_times = [
#         data[EGOBOX_VERSION][dim][num_points]
#         for num_points, dim in zip(nb_points, matrix_dimensions)
#     ]

#     plt.plot(
#         matrix_dimensions,
#         smt_times,
#         marker="o",
#         linestyle="-",
#         color="b",
#         label=SMT_VERSION,
#     )
#     plt.plot(
#         matrix_dimensions,
#         egobox_times,
#         marker="s",
#         linestyle="-",
#         color="r",
#         label=EGOBOX_VERSION,
#     )

#     plt.xlabel("Dimensions")
#     plt.ylabel("Temps (s)")
#     plt.title(f"Kriging {args} dimensions benchmark")
#     plt.legend()
#     plt.savefig(f"results/kriging/kriging_{args}_dimensions_lines.png")
#     plt.close()


def create_line_chart_kriging(matrix_dimensions, data, nb_points):
    plt.figure(figsize=(10, 6))

    smt_times = [
        data[SMT_VERSION][dim][num_points]
        for num_points, dim in zip(nb_points, matrix_dimensions)
    ]
    egobox_times = [
        data[EGOBOX_VERSION][dim][num_points]
        for num_points, dim in zip(nb_points, matrix_dimensions)
    ]

    plt.plot(
        matrix_dimensions,
        smt_times,
        marker="o",
        linestyle="-",
        color="b",
        label=SMT_VERSION,
    )
    plt.plot(
        matrix_dimensions,
        egobox_times,
        marker="s",
        linestyle="-",
        color="r",
        label=EGOBOX_VERSION,
    )

    plt.xlabel("Dimensions")
    plt.ylabel("Temps (s)")
    plt.title("Kriging benchmark (low & high dimensions)")
    plt.legend()
    plt.savefig(f"results/kriging/kriging_all_dimensions_{SMT_VERSION}_{EGOBOX_VERSION}.png")
    plt.close()


if __name__ == "__main__":
    args = parse_arguments()
    data = read_from_csv(CSV_FILENAME)
    dimensions = sort_dimensions(data, args.dimensions)
    print(dimensions)
    if args.dimensions == "low":
        create_chart(dimensions, data, NB_POINTS1, args.dimensions)

    if args.dimensions == "high":
        create_chart(dimensions, data, NB_POINTS2, args.dimensions)

    dimensions_low = sort_dimensions(data, "low")
    dimensions_high = sort_dimensions(data, "high")
    all_dimensions = dimensions_low + dimensions_high
    all_nb_points = NB_POINTS1 + NB_POINTS2

    create_line_chart_kriging(all_dimensions, data, all_nb_points)
