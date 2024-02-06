"""
Author: Antoine Averland <antoine.averland@onera.fr>
benchmark comparison between smt and egobox
"""

from smt.sampling_methods import LHS
import egobox as egx
import numpy as np
import timeit

#10/50/200/800/1500

matrice5 = np.full((5, 2), [0, 1])
matrice20 = np.full((20, 2), [0, 1])
matrice50 = np.full((50, 2), [0, 1])
matrice100 = np.full((100, 2), [0, 1])
matrice500 = np.full((500, 2), [0, 1])

list_xlimits = [matrice5, matrice20, matrice50, matrice100, matrice500]
#list_num_points = [10, 50, 200, 800, 1500]
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
        result_smt = timeit.timeit(lambda: smt_lhs(xlimits, num_points), number=5)
        average_time_smt = result_smt / 5
        list_time_smt.append(average_time_smt)
        print(f"je suis dans le bench de smt avec {xlimits} pour {num_points} points")

# Benchmark for EGObox
for xlimits in list_xlimits:
    for num_points in list_num_points:
        result_egob = timeit.timeit(lambda: egobox_lhs(xlimits, num_points), number=5)
        average_time_egob = result_egob / 5
        list_time_egobox.append(average_time_egob)
        print(f"je suis dans le bench de egobox avec {xlimits} pour {num_points} points")

# Affichage des résultats
for i, xlimits in enumerate(list_xlimits, start=0):
    for j, num_points in enumerate(list_num_points):
        idx = i * len(list_num_points) + j
        average_time_smt = list_time_smt[idx]
        average_time_egob = list_time_egobox[idx]
        print(f"Average time for xlimits {i} with {num_points} points for SMT: {average_time_smt} seconds")
        print(f"Average time for xlimits {i} with {num_points} points for EGObox: {average_time_egob} seconds")
        print()

