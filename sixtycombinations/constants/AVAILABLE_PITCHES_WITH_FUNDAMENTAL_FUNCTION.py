"""Collect all pitches which act as fundamentals within a spectral harmony."""

from sixtycombinations.constants import AVAILABLE_PITCHES

AVAILABLE_PITCHES_WITH_FUNDAMENTAL_FUNCTION = tuple(
    p for p in AVAILABLE_PITCHES if all([n <= 0 for n in p.exponents[1:]])
)
