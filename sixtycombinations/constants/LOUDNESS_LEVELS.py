"""Calculates Loudness that slowly rise.

This script assumes that doubling the loudness value doubles
the perceived loudness (therefore using an logarithmic scale).
"""

import math
import numpy as np

from sixtycombinations.constants import LOUDNESS_LEVEL_RANGE
from sixtycombinations.constants import N_LOUDNESS_LEVELS

max_n_steps = math.log2(LOUDNESS_LEVEL_RANGE[1] / LOUDNESS_LEVEL_RANGE[0])

LOUDNESS_LEVELS = tuple(
    LOUDNESS_LEVEL_RANGE[0] * (2 ** n_steps)
    for n_steps in np.linspace(0, max_n_steps, N_LOUDNESS_LEVELS, dtype=float)
)
