import itertools
import typing
import unittest

from sixtycombinations.constants import GROUPS


class HarmoniesTest(unittest.TestCase):
    @staticmethod
    def get_duration_of_cycle(cycle: typing.Tuple["Group"]) -> float:
        return sum(
            sum(
                n_phases * (1 / group.fundamental.frequency)
                for n_phases in (group.attack, group.sustain)
            )
            for group in cycle
        )

    def test_equal_duration_of_different_cycles(self):
        durations = tuple(self.get_duration_of_cycle(cycle) for cycle in GROUPS)
        for duration0, duration1 in itertools.combinations(durations, 2):
            self.assertEqual(duration0, duration1)

    def test_relative_start_times_add_up(self):
        duration = self.get_duration_of_cycle(GROUPS[0])
        for cycle in GROUPS:
            self.assertAlmostEqual(
                cycle[-1].relative_start_time
                + (
                    (cycle[-1].attack + cycle[-1].sustain)
                    * (1 / cycle[-1].fundamental.frequency)
                ),
                duration,
            )


if __name__ == "__main__":
    unittest.main()
