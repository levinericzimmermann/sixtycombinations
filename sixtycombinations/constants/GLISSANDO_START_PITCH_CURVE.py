"""Curve which defines the probability of each glissando start pitch interval."""

import expenvelope

from mutwo.parameters import pitches

from sixtycombinations import classes

GLISSANDO_START_PITCH_CURVE = classes.DynamicChoice(
    (
        pitches.JustIntonationPitch("8/9"),
        pitches.JustIntonationPitch("15/16"),
        pitches.JustIntonationPitch("24/25"),
        pitches.JustIntonationPitch("1/1"),
        pitches.JustIntonationPitch("25/24"),
        pitches.JustIntonationPitch("16/15"),
        pitches.JustIntonationPitch("9/8"),
    ),
    (
        # 8/9
        expenvelope.Envelope.from_points((0, 0.1), (1, 0.1)),
        # 15/16
        expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
        # 24/25
        expenvelope.Envelope.from_points((0, 0.5), (1, 0.5)),
        # 1/1
        expenvelope.Envelope.from_points((0, 1.2), (1, 1.2)),
        # 25/24
        expenvelope.Envelope.from_points((0, 0.2), (1, 0.2)),
        # 16/15
        expenvelope.Envelope.from_points((0, 0.15), (1, 0.15)),
        # 9/8
        expenvelope.Envelope.from_points((0, 0.01), (1, 0.01)),
    ),
)
