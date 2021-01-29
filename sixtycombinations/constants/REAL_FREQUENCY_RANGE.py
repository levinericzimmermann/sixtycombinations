"""Definition of the lowest and highest occuring frequencies.

May be slightly different to FREQUENCY_RANGE (which defines the allowed range).
"""

import functools
import operator

from sixtycombinations.constants import HARMONIES_IN_CORRECT_REGISTER

frequencies = tuple(
    pitch.frequency
    for pitch in functools.reduce(
        operator.add, functools.reduce(operator.add, HARMONIES_IN_CORRECT_REGISTER)
    )
)
REAL_FREQUENCY_RANGE = (min(frequencies), max(frequencies))
