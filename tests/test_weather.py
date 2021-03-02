import unittest

import numpy as np

from sixtycombinations import constants


class WeatherTest(unittest.TestCase):
    def test_get_value_at(self):
        for point in np.linspace(0, 0.99999, 100):
            self.assertTrue(
                constants.WEATHER.get_value_of_at("spectrality", point) is not None
            )
            self.assertTrue(
                constants.WEATHER.get_value_of_at("minimal_phases_per_sound", point)
            )
            self.assertTrue(constants.WEATHER.get_value_of_at("density", point))


if __name__ == "__main__":
    unittest.main()
