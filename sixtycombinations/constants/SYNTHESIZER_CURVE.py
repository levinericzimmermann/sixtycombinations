"""Curve which defines the probability of each csound instrument depending on time."""

import expenvelope

from sixtycombinations import classes

SYNTHESIZER_CURVE = classes.DynamicChoice(
    # 1 -> sine
    # 2 -> filtered noise
    (1, 2),
    (
        # sine
        expenvelope.Envelope.from_points((0, 1), (1, 1)),
        # filtered noise
        expenvelope.Envelope.from_points((0, 0.285), (1, 0.285)),
    ),
)
