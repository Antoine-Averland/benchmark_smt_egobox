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
list_smt = []
list_egobox = []
list_time_smt = []
list_time_egobox = []

def smt_lhs(xlimits):
    num = 10
    sampling = LHS(xlimits=xlimits, criterion="ese", random_state=42)
    doe1 = sampling(num)
    return doe1

def egobox_lhs(xlimits):
    xspecs = egx.to_specs(xlimits)
    doe2 = egx.lhs(xspecs, 10)
    return doe2

# Benchmark pour SMT
for xlimits in list_xlimits:
    result_smt = timeit.timeit(lambda: smt_lhs(xlimits), number=5)
    average_time_smt = result_smt / 5
    list_time_smt.append(average_time_smt)

# Benchmark pour EGObox
for xlimits in list_xlimits:
    result_egob = timeit.timeit(lambda: egobox_lhs(xlimits), number=5)
    average_time_egob = result_egob / 5
    list_time_egobox.append(average_time_egob)

# Affichage des résultats
for i, (average_time_smt, average_time_egob) in enumerate(zip(list_time_smt, list_time_egobox), start=1):
    print(f"Average time for xlimits {i} for SMT: {average_time_smt} seconds")
    print(f"Average time for xlimits {i} for EGObox: {average_time_egob} seconds")
    print()
