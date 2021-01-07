"""Definition of all loudspeakers that are used for the installation."""

import expenvelope

from sixtycombinations.classes import Loudspeaker

LOUDSPEAKERS = {
    loudspeaker.name: loudspeaker
    for loudspeaker in (
        Loudspeaker(
            "K50FL",
            expenvelope.Envelope.from_points(
                (0, 0),
                (50, 50),
                (100, 64),
                (200, 75),
                (500, 82),
                (1000, 78),
                (2000, 76),
                (5000, 80),
                (10000, 83.3),
                (20000, 79),
            ),
        ),
    )
}
