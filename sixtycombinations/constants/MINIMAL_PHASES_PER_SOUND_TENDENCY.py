"""This file defines how many phases each vibration should last at least (min)."""

import expenvelope

from sixtycombinations import classes

MINIMAL_PHASES_PER_SOUND_TENDENCY = classes.Tendency(
    expenvelope.Envelope.from_points((0, 40), (1, 40)),
    expenvelope.Envelope.from_points((0, 950), (1, 950)),
)
