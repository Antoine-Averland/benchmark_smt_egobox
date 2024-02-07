"""
Author: Antoine Averland <antoine.averland@onera.fr>
benchmark comparison between smt and egobox
"""

from smt.sampling_methods import LHS
import egobox as egx
import numpy as np
import timeit
import csv

matrix5 = np.full((5, 2), [0, 1])
matrix20 = np.full((20, 2), [0, 1])
matrix50 = np.full((50, 2), [0, 1])
matrix100 = np.full((100, 2), [0, 1])
matrix500 = np.full((500, 2), [0, 1])

list_xlimits = [matrix5, matrix20, matrix50, matrix100, matrix500]
#list_num_points = [10, 50, 200, 600, 1000]
list_num_points = [10, 13, 15]
list_smt = []
list_egobox = []
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

# Benchmark for SMT
for xlimits in list_xlimits:
    for num_points in list_num_points:
        print(f"je suis dans le bench de smt avec {xlimits} pour {num_points} points")
        result_smt = timeit.timeit(lambda: smt_lhs(xlimits, num_points), number=5)
        average_time_smt = result_smt / 5
        list_time_smt.append(average_time_smt)

# Benchmark for EGObox
for xlimits in list_xlimits:
    for num_points in list_num_points:
        print(f"je suis dans le bench de egobox avec {xlimits} pour {num_points} points")
        result_egob = timeit.timeit(lambda: egobox_lhs(xlimits, num_points), number=5)
        average_time_egob = result_egob / 5
        list_time_egobox.append(average_time_egob)

# Affichage des résultats
for i, xlimits in enumerate(list_xlimits, start=0):
    for j, num_points in enumerate(list_num_points):
        idx = i * len(list_num_points) + j
        average_time_smt = list_time_smt[idx]
        average_time_egob = list_time_egobox[idx]
        print(f"Average time for xlimits {i} with {num_points} points for SMT: {average_time_smt} seconds")
        print(f"Average time for xlimits {i} with {num_points} points for EGObox: {average_time_egob} seconds")
        print()

#écriture dans le csv
csv_filename = "results_benchmark.csv"

with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    headers = ['Program', 'Matrix', 'Num_Points', 'Average_Time_(seconds)']
    writer.writerow(headers)

    for i, xlimits in enumerate(list_xlimits, start=0):
        for j, num_points in enumerate(list_num_points):
            idx = i * len(list_num_points) + j
            average_time_smt = list_time_smt[idx]
            row = ['SMT', f'Matrix{i}', num_points, '{:3f}'.format(average_time_smt)]
            writer.writerow(row)

    # Écrire les résultats pour EGObox
    for i, xlimits in enumerate(list_xlimits, start=0):
        for j, num_points in enumerate(list_num_points):
            idx = i * len(list_num_points) + j
            average_time_egob = list_time_egobox[idx]
            row = ['EGObox', f'Matrix{i}', num_points, '{:.3f}'.format(average_time_egob)]
            writer.writerow(row)
