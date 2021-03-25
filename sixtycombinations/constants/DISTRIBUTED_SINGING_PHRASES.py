import operator

import expenvelope
from mutwo.utilities import tools

from sixtycombinations import classes
from sixtycombinations.constants import SINGING_PHRASES

# for value > 1: longer transition than stable state, for value < 1: longer stable state
n_phrases = len(SINGING_PHRASES)
TRANSITION_FACTOR = 0.7
DURATION_OF_STABLE_STATE = (1 / n_phrases) / (1 + TRANSITION_FACTOR)

assert (
    DURATION_OF_STABLE_STATE + (DURATION_OF_STABLE_STATE * TRANSITION_FACTOR)
) * n_phrases == 1

absolute_time_per_point = tools.accumulate_from_zero(
    (DURATION_OF_STABLE_STATE, DURATION_OF_STABLE_STATE * TRANSITION_FACTOR) * n_phrases
)
points_per_phrase = [[] for _ in SINGING_PHRASES]

for nth_point, absolute_time in enumerate(absolute_time_per_point):
    nth_stable_phrase = (nth_point // 2) % n_phrases
    points_per_phrase[nth_stable_phrase].append((absolute_time, 1))

    if nth_point % 2:
        neighbour_phrase = (nth_stable_phrase - 1) % n_phrases
    else:
        neighbour_phrase = (nth_stable_phrase + 1) % n_phrases

    points_per_phrase[neighbour_phrase].append((absolute_time, 0))

for points in points_per_phrase:
    if points[0][0] != 0:
        points.insert(0, (0, 0))

    if points[-1][0] != 1:
        points.append((1, 0))

    points.sort(key=operator.itemgetter(0))

curves = tuple(
    expenvelope.Envelope.from_points(*points) for points in points_per_phrase
)

DISTRIBUTED_SINGING_PHRASES = classes.DynamicChoice(
    SINGING_PHRASES, curves, random_seed=1995
)
