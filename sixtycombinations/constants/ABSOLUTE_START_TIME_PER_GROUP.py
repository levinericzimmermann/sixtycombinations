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
