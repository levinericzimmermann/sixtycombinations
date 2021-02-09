"""This file defines how many phases each vibration should last at least (min)."""

import expenvelope

from sixtycombinations import classes

MINIMAL_PHASES_PER_SOUND_TENDENCY = classes.Tendency(
    # expenvelope.Envelope.from_points((0, 40), (1, 40)),
    # expenvelope.Envelope.from_points((0, 950), (1, 950)),
    expenvelope.Envelope.from_points((0, 8), (1, 8)),
    expenvelope.Envelope.from_points((0, 9000), (1, 9000)),
    # expenvelope.Envelope.from_points((0, 250), (1, 250)),
    # expenvelope.Envelope.from_points((0, 27000), (1, 27000)),
)
