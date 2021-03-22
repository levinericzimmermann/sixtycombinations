from mutwo.utilities import tools

from sixtycombinations.constants import DURATION
from sixtycombinations.constants import GROUPS

ABSOLUTE_START_TIME_PER_GROUP = [0]
for nth_cycle, group in zip(range(1, 3), GROUPS[1:]):
    previous_group = GROUPS[nth_cycle - 1]
    current_group = GROUPS[nth_cycle]
    start_time = ABSOLUTE_START_TIME_PER_GROUP[nth_cycle - 1] + (
        (
            (previous_group[0].attack * (1 / previous_group[0].fundamental.frequency))
            - (current_group[0].attack * (1 / current_group[0].fundamental.frequency))
        )
        / 2
    )
    ABSOLUTE_START_TIME_PER_GROUP.append(start_time)

# make immutable
ABSOLUTE_START_TIME_PER_GROUP = tuple(ABSOLUTE_START_TIME_PER_GROUP)


for nth_cycle, cycle in enumerate(GROUPS):
    absolue_start_time = ABSOLUTE_START_TIME_PER_GROUP[nth_cycle]

    for group in cycle:
        period_duration = 1 / group.fundamental.frequency
        duration_per_state = tuple(
            getattr(group, state) * period_duration
            for state in ("attack", "sustain", "release")
        )

        group_start_time = absolue_start_time + group.relative_start_time
        start_time_per_state = tuple(
            start_time % DURATION
            for start_time in tools.accumulate_from_n(
                duration_per_state, group_start_time
            )
        )[:-1]
        group.absolute_start_time_per_state = start_time_per_state
