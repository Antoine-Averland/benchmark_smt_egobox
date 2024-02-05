"""
Author: Antoine Averland <antoine.averland@onera.fr>
benchmark comparison between smt and egobox
"""

from smt.sampling_methods import LHS
import egobox as egx
import numpy as np


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

__benchmarks__ = [
    (smt_lhs(), egobox_lhs(), "Compare the lhs from smt with the lhs from egobox")
]