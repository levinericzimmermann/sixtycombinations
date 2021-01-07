from sixtycombinations.constants import GROUPS

# The complete duration of one loop in seconds.
DURATION = sum(
    sum(
        n_phases * (1 / group.fundamental.frequency)
        for n_phases in (group.attack, group.sustain)
    )
    for group in GROUPS[0]
)
