import unittest

from sixtycombinations.constants import HARMONIES


class HarmoniesTest(unittest.TestCase):
    @staticmethod
    def get_intervals_to_first_pitch(pitches: tuple) -> tuple:
        return tuple(pitch - pitches[0] for pitch in pitches)

    def test_pitch_order(self):
        for bar in HARMONIES.pitches_per_voice_per_bar:
            for voice in bar:
                intervals = self.get_intervals_to_first_pitch(voice)

                # make sure any of the resulting intervals belong to
                # the asked overtone series
                for interval in intervals:
                    self.assertTrue(
                        any(
                            (
                                float(interval.ratio) in HARMONIES.harmonic_primes,
                                interval.ratio == 1,
                            )
                        )
                    )

                # make sure the order of the overtone series is ascending
                for interval0, interval1 in zip(intervals, intervals[1:]):
                    self.assertLess(interval0, interval1)


if __name__ == "__main__":
    unittest.main()
