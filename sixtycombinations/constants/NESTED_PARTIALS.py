"""Nested structure of partials.

The structure is nested in:

    -> cycles
        -> speakers
            -> a/b

Where
    - 'cycles' represent the three different cycles of groups
    - 'speakers' represent the specific loudspeakers within one group
    - 'a/b' represent two simultaneous events that are played from the
      same speaker. This is necessary because during transitions between
      two groups one speaker plays two sine waves simultaneously

"""

from mutwo.events import basic

from sixtycombinations.classes import Partial
from sixtycombinations.constants import GROUPS
from sixtycombinations.constants import PITCH_TO_LOUDSPEAKER_MAPPING
from sixtycombinations.constants import RING_POSITION_TO_LOUDSPEAKER

NESTED_PARTIALS = basic.SimultaneousEvent(
    [
        basic.SimultaneousEvent(
            [
                basic.SimultaneousEvent(
                    [basic.SequentialEvent([]), basic.SequentialEvent([])]
                )
                for nth_speaker in cycle
            ]
        )
        for cycle in RING_POSITION_TO_LOUDSPEAKER
    ]
)

for nth_cycle, cycle in enumerate(GROUPS):
    is_first = True
    for nth_group, group in enumerate(cycle):
        if is_first:
            n_phases_rest = group.attack + group.sustain
            is_first = False
        else:
            n_phases_rest = group.sustain

        rest = basic.SimpleEvent(n_phases_rest * (1 / group.fundamental.frequency))

        common_pitch_data_with_previous_harmony = (
            group.common_pitch_data_with_previous_harmony
        )
        common_pitch_data_with_next_harmony = group.common_pitch_data_with_next_harmony

        pitch_to_loudspeaker_mapping = PITCH_TO_LOUDSPEAKER_MAPPING[nth_cycle][
            nth_group % len(PITCH_TO_LOUDSPEAKER_MAPPING[nth_cycle])
        ]
        a_or_b = nth_group % 2
        for nth_pitch, pitch in enumerate(group.harmony):
            nth_loudspeaker = pitch_to_loudspeaker_mapping.index(nth_pitch)
            nth_partial = int((pitch - group.fundamental).ratio)
            is_connection_pitch_to_previous_harmony = (
                pitch == common_pitch_data_with_previous_harmony[0][1]
            )
            is_connection_pitch_to_next_harmony = (
                pitch == common_pitch_data_with_next_harmony[0][0]
            )
            attack, sustain, release = (
                n_phases * nth_partial
                for n_phases in (group.attack, group.sustain, group.release)
            )
            partial = Partial(
                pitch,
                attack,
                sustain,
                release,
                nth_pitch,
                nth_partial,
                is_connection_pitch_to_previous_harmony,
                is_connection_pitch_to_next_harmony,
                RING_POSITION_TO_LOUDSPEAKER[nth_cycle][nth_loudspeaker],
                tuple(state[nth_pitch] for state in group.rhythmical_data_per_state),
                nth_cycle,
                group.absolute_start_time_per_state
            )

            # add partial
            NESTED_PARTIALS[nth_cycle][nth_loudspeaker][a_or_b].append(partial)

            # add rest
            NESTED_PARTIALS[nth_cycle][nth_loudspeaker][not a_or_b].append(
                rest.destructive_copy()
            )
