"""Curve for bandwidth of resonance filter for filtered noise instrument."""

import expenvelope

BANDWIDTH = expenvelope.Envelope.from_points(
    (0, 0.91),
    (1, 0.91),
)
