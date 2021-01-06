import itertools
import typing
import unittest

from sixtycombinations.constants import GROUPS


class HarmoniesTest(unittest.TestCase):
    def test_equal_duration_of_different_cycles(self):
        def get_duration_of_cycle(cycle: typing.Tuple["Group"]) -> float:
            return sum(
                sum(
                    n_phases * (1 / group.fundamental.frequency)
                    for n_phases in (group.attack, group.sustain)
                )
                for group in cycle
            )

        durations = tuple(get_duration_of_cycle(cycle) for cycle in GROUPS)
        for duration0, duration1 in itertools.combinations(durations, 2):
            self.assertEqual(duration0, duration1)


if __name__ == "__main__":
    unittest.main()
