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
    tuple(LOUDSPEAKERS["K50FL"] for _ in range(6)),
    tuple(LOUDSPEAKERS["K50FL"] for _ in range(5)),
    tuple(LOUDSPEAKERS["K50FL"] for _ in range(4)),
)
