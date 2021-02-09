"""Definition of filter quality.

Expected values are in the range (-15, 15) where 15 makes the strongest
filter and -15 the weakest filter.
"""

import expenvelope

FILTER_Q = expenvelope.Envelope.from_points((0, -16), (1, -16),)
# FILTER_Q = expenvelope.Envelope.from_points(
#     (0, 15), (0.03, -15), (0.08, 15), (0.11, -15), (1, 15)
# )

# import math
# 
# 
# def make_repeating_sine(duration: float = 0.05, period=1):
#     factor = period / duration
# 
#     def repsine(time: float) -> float:
#         return -15 + (30 * math.sin(math.pi * (factor * (time % duration))))
# 
#     return repsine
# 
# 
# FILTER_Q = expenvelope.Envelope.from_function(make_repeating_sine())
