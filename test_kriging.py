import unittest
import numpy as np
from smt.surrogate_models import KRG
from smt.sampling_methods import LHS
from smt.problems import Sphere
from smt.surrogate_models import GPX


class TestKriging(unittest.TestCase):
    def test_kriging(self):
        ndim = 10
        num = 200
        problem = Sphere(ndim=ndim)
        xlimits = problem.xlimits
        sampling = LHS(xlimits=xlimits, criterion="ese", random_state=42)

        xt = sampling(num)
        yt = problem(xt)

        sm1 = KRG()
        sm1.set_training_values(xt, yt)
        sm1.train()

        sm2 = GPX()
        sm2.set_training_values(xt, yt)
        sm2.train()

        xe = sampling(10)
        ye = problem(xe)

        ytest1 = sm1.predict_values(xe)
        e_error1 = np.linalg.norm(ytest1 - ye) / np.linalg.norm(ye)
        print(e_error1)

        ytest2 = sm2.predict_values(xe)
        e_error2 = np.linalg.norm(ytest2 - ye) / np.linalg.norm(ye)
        print(e_error2)

        self.assertAlmostEqual(e_error1, e_error2, places=1)


if __name__ == "__main__":
    unittest.main()
