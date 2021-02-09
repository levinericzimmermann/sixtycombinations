"""
"""

from sixtycombinations.constants import HARMONIES_IN_CORRECT_REGISTER
from sixtycombinations.constants import TRANSITION_PHASES_EXPONENT
from sixtycombinations.constants import TRANSITION_PHASES_FACTOR


def detect_how_many_phases_of_fundamental_during_transition(
    pitches0: tuple, pitches1: tuple, nth_cycle: int
) -> tuple:
    common_pitch = None
    for pitch0 in pitches0:
        for pitch1 in pitches1:
            if pitch0.exponents[1:] == pitch1.exponents[1:]:
                common_pitch = (pitch0, pitch1)
                break

    assert common_pitch

    prime0, prime1 = (
        int((pitch - pitches[0]).ratio)
        for pitch, pitches in zip(common_pitch, (pitches0, pitches1))
    )

    product = (prime0 ** TRANSITION_PHASES_EXPONENT) * (
        prime1 ** TRANSITION_PHASES_EXPONENT
    ) * TRANSITION_PHASES_FACTOR[nth_cycle]

    nth_partials = [product / prime1, product / prime0]

    # compensate octave differences
    try:
        n_octaves_difference = (common_pitch[0] - common_pitch[1]).exponents[0]
    except IndexError:
        n_octaves_difference = 0
    if n_octaves_difference > 0:
        nth_partials[1] *= 2 ** n_octaves_difference
    elif n_octaves_difference < 0:
        nth_partials[0] *= 2 ** abs(n_octaves_difference)

    return tuple(reversed(nth_partials))


TRANSITION_PHASES = []

for nth_cycle, cycle in enumerate(HARMONIES_IN_CORRECT_REGISTER):

    transitions = [[None, None] for _ in cycle]
    for index, pitches0, pitches1 in zip(
        range(len(cycle)), cycle, cycle[1:] + cycle[:1]
    ):
        n_phases0, n_phases1 = detect_how_many_phases_of_fundamental_during_transition(
            pitches0, pitches1, nth_cycle
        )
        transitions[index][1] = n_phases0
        try:
            transitions[index + 1][0] = n_phases1
        except IndexError:
            transitions[0][0] = n_phases1

    TRANSITION_PHASES.append(tuple(tuple(item) for item in transitions))

TRANSITION_PHASES = tuple(TRANSITION_PHASES)
