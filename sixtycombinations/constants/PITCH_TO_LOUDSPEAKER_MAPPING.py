"""
"""

import itertools
import typing

from sixtycombinations.constants import HARMONIES_IN_CORRECT_REGISTER


def rotate(iterable: typing.Iterable, n_steps: int) -> typing.Iterable:
    return iterable[-n_steps:] + iterable[:-n_steps]


mapping_cycles_per_ring = (
    # where loudspeaker -> partial index
    # (e.g. second element == 2 means that the second speaker plays
    # the third partial of a sound)
    itertools.cycle(((0, 2, 4, 1, 3, 5), (0, 5, 3, 1, 4, 2))),
    itertools.cycle(((0, 2, 4, 1, 3), (0, 3, 1, 4, 2))),
    itertools.cycle(((0, 3, 1, 2), (0, 2, 1, 3))),
)

# definition of global variable, fill it already up with the data for the outer cycle
PITCH_TO_LOUDSPEAKER_MAPPING = [
    # outer cycle:
    # -> always set fundamental to the first speaker, because there is only one
    # subwoofer and this subwoofer is at position 0.
    tuple(
        next(mapping_cycles_per_ring[0]) for harmony in HARMONIES_IN_CORRECT_REGISTER[0]
    ),
    [],
    [],
]

# add the second and the third cycles
for nth_cycle, harmonies in enumerate(HARMONIES_IN_CORRECT_REGISTER):
    if nth_cycle > 0:
        lower_pitch_group_index_divider = len(harmonies) // len(
            HARMONIES_IN_CORRECT_REGISTER[nth_cycle - 1]
        )
        for nth_harmony, harmony in enumerate(harmonies):
            simultaneous_lower_pitch_group_index = (
                nth_harmony // lower_pitch_group_index_divider
            )
            simultaneous_lower_pitch_group = HARMONIES_IN_CORRECT_REGISTER[
                nth_cycle - 1
            ][simultaneous_lower_pitch_group_index]
            simultaneous_lower_pitch_group_loudspeaker_mapping = PITCH_TO_LOUDSPEAKER_MAPPING[
                nth_cycle - 1
            ][
                simultaneous_lower_pitch_group_index
            ]
            fundamental_index, *_ = tuple(
                pitch_index
                for pitch_index, pitch in enumerate(simultaneous_lower_pitch_group)
                if pitch.exponents[1:] == harmony[0].exponents[1:]
            )
            fundamental_loudspeaker_position = simultaneous_lower_pitch_group_loudspeaker_mapping.index(
                fundamental_index
            )
            if fundamental_loudspeaker_position >= len(harmony):
                fundamental_loudspeaker_position = 0

            mapping = next(mapping_cycles_per_ring[nth_cycle])
            PITCH_TO_LOUDSPEAKER_MAPPING[nth_cycle].append(
                rotate(mapping, fundamental_loudspeaker_position)
            )


PITCH_TO_LOUDSPEAKER_MAPPING = tuple(
    map(lambda mapping: tuple(mapping), PITCH_TO_LOUDSPEAKER_MAPPING)
)
