"""
Author: Antoine Averland <antoine.averland@onera.fr>
benchmark comparison between smt and egobox
"""

from smt.sampling_methods import LHS
import egobox as egx
import numpy as np
import timeit

matrice5 = np.full((5, 2), [0, 1])
matrice20 = np.full((20, 2), [0, 1])
matrice50 = np.full((50, 2), [0, 1])
matrice100 = np.full((100, 2), [0, 1])


def smt_lhs():
    xlimits = np.array([[0.0, 4.0], [0.0, 3.0]])
    num = 10
    sampling = LHS(xlimits=xlimits, criterion="ese", random_state=42)
    doe1 = sampling(num)
    return doe1

def egobox_lhs():
    xspecs = egx.to_specs([[0.0, 4.0], [0.0, 3.0]])
    doe2 = egx.lhs(xspecs, 10)
    return doe2

#benchmark
result_smt = timeit.timeit('smt_lhs()', setup ='from __main__ import smt_lhs', number = 3)
average_time_smt = result_smt/3

result_egob = timeit.timeit('egobox_lhs()', setup ='from __main__ import egobox_lhs', number = 3)
average_time_egob = result_egob/3

print("Average time for smt:")
print(average_time_smt)
print("Average time for egobox:")
print(average_time_egob)