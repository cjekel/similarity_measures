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
    unittest.main()
