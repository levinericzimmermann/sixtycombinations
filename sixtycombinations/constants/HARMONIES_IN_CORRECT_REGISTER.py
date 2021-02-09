"""This script separates and registers the content of pitches_per_voice_per_bar.

The script also sets the global CONCERT_PITCH, depending on the register calculation.

The pitches_per_bar_per_voice attribute get separated into three cycles
(where the first cycle consists of 5 elements, the second cycle consists of
20 elements and the third cycle consists of 60 elements).

Furthermore the pitches in every cycle gets registered so that the deepest
appearing frequency >= FREQUENCY_RANGE[0] and the highest appearing
frequency <= FREQUENCY_RANGE[1].
"""

from mutwo.parameters import pitches
from mutwo.parameters import pitches_constants

from sixtycombinations.constants import FREQUENCY_RANGE
from sixtycombinations.constants import HARMONIES

# ####################################
# (1) separate into cycles
# ####################################
pitch_groups_per_cycle = tuple(
    tuple(
        HARMONIES.pitches_per_voice_per_bar[nth_bar][nth_voice]
        for nth_bar in range(0, 60, every_nth_bar_there_is_a_new_pitch_group)
    )
    for nth_voice, every_nth_bar_there_is_a_new_pitch_group in enumerate(
        (60 // 5, 60 // 20, 60 // 60)
    )
)


# ####################################
# (2) find lowest pitch in first cycle to set global CONCERT_PITCH
# ####################################
lowest_pitch_in_first_cycle = min(
    map(
        lambda x: x[0].normalize(mutate=False),  # normalize first pitch
        pitch_groups_per_cycle[0],  # analyse the first cycle
    )
)
# concert pitch for 1/1
pitches_constants.DEFAULT_CONCERT_PITCH = float(
    FREQUENCY_RANGE[0] / lowest_pitch_in_first_cycle.ratio
)


# ####################################
# (3) register pitches in each cycle
# ####################################
HARMONIES_IN_CORRECT_REGISTER = [[], [], []]


def make_registered_pitch_group_from_fundamental_and_pitch_group(
    fundamental: pitches.JustIntonationPitch, pitch_group: tuple
) -> tuple:
    intervals = (pitch - pitch_group[0] for pitch in pitch_group)
    registered_pitch_group = tuple(fundamental + interval for interval in intervals)
    return registered_pitch_group


# lowest cycle
for pitch_group_in_lowest_cycle in pitch_groups_per_cycle[0]:
    fundamental = pitches.JustIntonationPitch(
        pitch_group_in_lowest_cycle[0].normalize(mutate=False).exponents
    )
    registered_pitch_group_in_lowest_cycle = make_registered_pitch_group_from_fundamental_and_pitch_group(
        fundamental, pitch_group_in_lowest_cycle
    )
    HARMONIES_IN_CORRECT_REGISTER[0].append(registered_pitch_group_in_lowest_cycle)

# central & highest cycle
for nth_pitch_groups, pitch_groups in enumerate(pitch_groups_per_cycle[1:]):
    lower_pitch_group_index_divider = len(pitch_groups) // len(
        pitch_groups_per_cycle[nth_pitch_groups]
    )
    for nth_pitch_group, pitch_group_in_central_cycle in enumerate(pitch_groups):
        simultaneous_lower_pitch_group_index = (
            nth_pitch_group // lower_pitch_group_index_divider
        )
        simultaneous_lower_pitch_group = HARMONIES_IN_CORRECT_REGISTER[
            nth_pitch_groups
        ][simultaneous_lower_pitch_group_index]
        fundamental, *_ = tuple(
            pitch
            for pitch in simultaneous_lower_pitch_group
            if pitch.exponents[1:] == pitch_group_in_central_cycle[0].exponents[1:]
        )
        registered_pitch_group_in_central_cycle = make_registered_pitch_group_from_fundamental_and_pitch_group(
            fundamental, pitch_group_in_central_cycle
        )
        while (
            registered_pitch_group_in_central_cycle[-1].frequency > FREQUENCY_RANGE[1]
        ):
            [
                pitch.subtract(pitches.JustIntonationPitch("2/1"))
                for pitch in registered_pitch_group_in_central_cycle
            ]

        HARMONIES_IN_CORRECT_REGISTER[nth_pitch_groups + 1].append(
            registered_pitch_group_in_central_cycle
        )

HARMONIES_IN_CORRECT_REGISTER = tuple(
    map(lambda harmonies: tuple(harmonies), HARMONIES_IN_CORRECT_REGISTER)
)
