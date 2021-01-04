import unittest

from mutwo.parameters import pitches

from sixtycombinations.constants import HARMONIES_IN_CORRECT_REGISTER
from sixtycombinations.constants import TRANSITION_PHASES


class TransitionPhases(unittest.TestCase):
    @staticmethod
    def calculate_duration(pitch: pitches.JustIntonationPitch, n_phases: int) -> float:
        return (1 / pitch.frequency) * n_phases

    def test_equal_transition_duration(self):
        for transition_cycle, pitch_cycle in zip(
            TRANSITION_PHASES, HARMONIES_IN_CORRECT_REGISTER
        ):
            for pitches0, pitches1, transition0, transition1 in zip(
                pitch_cycle,
                pitch_cycle[1:] + pitch_cycle[:1],
                transition_cycle,
                transition_cycle[1:] + transition_cycle[:1],
            ):
                self.assertAlmostEqual(
                    *tuple(
                        self.calculate_duration(pitch, n_phases)
                        for pitch, n_phases in zip(
                            (pitches0[0], pitches1[0]), (transition0[1], transition1[0])
                        )
                    )
                )


if __name__ == "__main__":
    unittest.main()
