"""
Author: Antoine Averland <antoine.averland@onera.fr>
benchmark comparison between smt and egobox
"""

from smt.sampling_methods import LHS
import egobox as egx
import numpy as np
import timeit
import csv

dimensions = [(5, 2), (20, 2), (50, 2), (100, 2), (500, 2)]

list_xlimits = [np.full(dim, [0, 1]) for dim in dimensions]

list_num_points = [10, 50, 100, 250, 500, 1000]
# list_num_points = [10, 13, 15]


list_time_smt = []
list_time_egobox = []


def smt_lhs(xlimits, num_points):
    sampling = LHS(xlimits=xlimits, criterion="ese", random_state=42)
    doe1 = sampling(num_points)
    return doe1


def egobox_lhs(xlimits, num_points):
    xspecs = egx.to_specs(xlimits)
    doe2 = egx.lhs(xspecs, num_points)
    return doe2


if __name__ == "__main__":
    # Benchmark for SMT
    for xlimits in list_xlimits:
        for num_points in list_num_points:
            print(
                f"je suis dans le bench de smt avec {xlimits} pour {num_points} points"
            )
            result_smt = timeit.timeit(lambda: smt_lhs(xlimits, num_points), number=5)
            average_time_smt = result_smt / 5
            list_time_smt.append(average_time_smt)

    # Benchmark for EGObox
    for xlimits in list_xlimits:
        for num_points in list_num_points:
            print(
                f"je suis dans le bench de egobox avec {xlimits} pour {num_points} points"
            )
            result_egob = timeit.timeit(
                lambda: egobox_lhs(xlimits, num_points), number=5
            )
            average_time_egob = result_egob / 5
            list_time_egobox.append(average_time_egob)

    # print of the results
    for i, xlimits in enumerate(list_xlimits, start=0):
        for j, num_points in enumerate(list_num_points):
            idx = i * len(list_num_points) + j
            average_time_smt = list_time_smt[idx]
            average_time_egob = list_time_egobox[idx]
            print(
                f"Average time for xlimits {i} with {num_points} points for SMT: {average_time_smt} seconds"
            )
            print(
                f"Average time for xlimits {i} with {num_points} points for EGObox: {average_time_egob} seconds"
            )
            print()

    # writing in csv file
    csv_filename = "results_benchmark.csv"

    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        headers = ["Program", "Matrix", "Num_Points", "Average_Time_(seconds)"]
        writer.writerow(headers)

        for i, xlimits in enumerate(list_xlimits, start=0):
            for j, num_points in enumerate(list_num_points):
                idx = i * len(list_num_points) + j
                average_time_smt = list_time_smt[idx]
                row = [
                    "SMT",
                    f"{xlimits.shape}",
                    num_points,
                    "{:3f}".format(average_time_smt),
                ]
                writer.writerow(row)

        for i, xlimits in enumerate(list_xlimits, start=0):
            for j, num_points in enumerate(list_num_points):
                idx = i * len(list_num_points) + j
                average_time_egob = list_time_egobox[idx]
                row = [
                    "EGObox",
                    f"{xlimits.shape}",
                    num_points,
                    "{:.3f}".format(average_time_egob),
                ]
                writer.writerow(row)
