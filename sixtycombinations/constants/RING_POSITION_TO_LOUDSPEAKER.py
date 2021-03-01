"""This file allocates ring positions to loudspeaker types.

RING_POSITION_TO_LOUDSPEAKER[RING][POSITION]

where RING =
    0 -> outer cycle
    1 -> central cycle
    2 -> inner cycle

where POSITION =
    0 - 5 (for outer cycle)
    0 - 4 (for central cycle)
    0 - 3 (for inner cycle)

    and where all 0 from the different cycles
    are as close as possible
"""

from sixtycombinations.constants import LOUDSPEAKERS

RING_POSITION_TO_LOUDSPEAKER = (
    tuple(
        LOUDSPEAKERS[name]
        for name in ("WS25E", "FRS7S", "FRS7S", "HW806", "FRS7S", "FRS7S")
    ),
    tuple(LOUDSPEAKERS[name] for name in ("K50FL", "FRS7S", "K50FL", "HW806", "K50FL")),
    tuple(LOUDSPEAKERS[name] for name in ("K50FL", "K50FL", "K50FL", "K50FLS")),
)
