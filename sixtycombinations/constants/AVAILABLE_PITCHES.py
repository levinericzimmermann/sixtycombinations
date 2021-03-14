"""Define a tuple which contains all available pitches for the installation."""

import functools
import operator

from mutwo.utilities import tools

from sixtycombinations.constants import HARMONIES_IN_CORRECT_REGISTER

AVAILABLE_PITCHES = tuple(
    sorted(
        tools.uniqify_iterable(
            p.normalize(mutate=False)
            for p in functools.reduce(
                operator.add,
                (
                    functools.reduce(operator.add, group)
                    for group in HARMONIES_IN_CORRECT_REGISTER
                ),
            )
        )
    )
)
