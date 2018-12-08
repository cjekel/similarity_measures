import numpy as np
import unittest
import similaritymeasures


class TestEverything(unittest.TestCase):

    def test_c1_c2_area(self):
        area = similaritymeasures.area_between_two_curves(curve1, curve2)
        self.assertTrue(area, 1.0)

    def test_c3_c4_area(self):
        area = similaritymeasures.area_between_two_curves(curve3, curve4)
        self.assertTrue(area, 1.0)

    def test_c1_c2_pcm(self):
        pcm = similaritymeasures.pcm(curve1, curve2)
        self.assertTrue(pcm, np.nan)

    def test_c3_c4_pcm(self):
        pcm = similaritymeasures.pcm(curve3, curve4)
        self.assertTrue(pcm, 50.0)

    def test_c1_c2_df(self):
        df = similaritymeasures.frechet_dist(curve1, curve2)
        self.assertTrue(df, 1.0)

    def test_c3_c4_df(self):
        df = similaritymeasures.frechet_dist(curve3, curve4)
        self.assertTrue(df, 1.0)

    def test_c1_c2_cl(self):
        cl = similaritymeasures.curve_length_measure(curve1, curve2)
        self.assertTrue(cl, 4.054651081081643)

    def test_c3_c4_cl(self):
        cl = similaritymeasures.curve_length_measure(curve3, curve4)
        self.assertTrue(cl, 10.986122886681098)

    def test_P_Q_dtw(self):
        d = similaritymeasures.dtw(P, Q)
        self.assertTrue(d, 3.0)

    def test_c5_c6_dtw(self):
        d = similaritymeasures.dtw(curve5, curve6)
        self.assertTrue(np.isclose(d, 9000.0))

    def test_c5_c6_df(self):
        df = similaritymeasures.frechet_dist(curve5, curve6)
        self.assertTrue(np.isclose(df, 90.0))


if __name__ == '__main__':
    # let's just define some data
    x1 = np.linspace(0.0, 1.0, 100)
    y1 = np.ones(100)*2
    x2 = np.linspace(0.0, 1.0, 50)
    y2 = np.ones(50)

    curve1 = np.array((x1, y1)).T
    curve2 = np.array((x2, y2)).T

    x1 = np.linspace(0.0, 1.0, 100)
    y1 = x1
    x2 = np.linspace(0.0, 1.0, 50)
    y2 = x2+1.0

    curve3 = np.array((x1, y1)).T
    curve4 = np.array((x2, y2)).T

    P = np.array([[0, 0], [1, 1], [2, 2]])
    Q = P.copy()
    Q[:, 1] = Q[:, 1] + 1

    r1 = 10
    r2 = 100
    theta = np.linspace(0.0, 2.0*np.pi, 100)
    x1 = np.cos(theta)*r1
    x2 = np.cos(theta)*r2
    y1 = np.sin(theta)*r1
    y2 = np.sin(theta)*r2
    curve5 = np.array((x1, y1)).T
    curve6 = np.array((x2, y2)).T

    unittest.main()
